import argparse
import asyncio
import json
import logging
import os
import signal
import sys
from asyncio import Queue
from datetime import datetime, timezone
from typing import Annotated, List, Union

import tornado.escape
import tornado.ioloop
import tornado.web
from annotated_types import Gt
from jupyter_client.asynchronous.client import AsyncKernelClient
from jupyter_client.manager import AsyncKernelManager
from pydantic import BaseModel

# Shell Jupyter message types
JupyterMessageTypeExecuteRequest = "execute_request"
JupyterMessageTypeExecuteReply = "execute_reply"

# IOPub Jupyter message types
JupyterMessageTypeStream = "stream"
JupyterMessageTypeDisplayData = "display_data"
JupyterMessageTypeExecuteResult = "execute_result"
JupyterMessageTypeError = "error"
JupyterMessageTypeStatus = "status"

# Supported Jupyter message types (IOPub only)
JupyterSupportedMessageTypes = [
    JupyterMessageTypeStream,
    JupyterMessageTypeDisplayData,
    JupyterMessageTypeExecuteResult,
    JupyterMessageTypeError,
    JupyterMessageTypeStatus,
]

# Kernel execution states
JupyterExecutionStateBusy = "busy"
JupyterExecutionStateIdle = "idle"
JupyterExecutionStateStarting = "starting"

# Saturn execution event types
ExecutionEventTypeStream = "stream"
ExecutionEventTypeDisplayData = "display_data"
ExecutionEventTypeError = "error"

# Saturn execution statuses
ExecutionStatusOK = "ok"
ExecutionStatusTimeout = "timeout"


class ExecutionEventStream(BaseModel):
    stream: str
    text: str


class ExecutionEventDisplayData(BaseModel):
    variants: dict


class ExecutionEventError(BaseModel):
    ename: str
    evalue: str
    traceback: list[str]


class ExecutionEvent(BaseModel):
    type: str
    timestamp: str  # RFC3339
    data: Union[
        ExecutionEventStream,
        ExecutionEventDisplayData,
        ExecutionEventError,
    ]


class ExecuteRequest(BaseModel):
    code: str
    timeout_secs: Annotated[int, Gt(0)]


class ExecuteResponse(BaseModel):
    status: str
    events: List[ExecutionEvent]


class PingResponse(BaseModel):
    last_activity: str  # RFC3339


class Error(BaseModel):
    error: str


def datetime_to_rfc3339(dt: datetime) -> str:
    """Convert a datetime to an RFC3339 formatted string."""
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def rfc3339_to_datetime(date_string: str) -> datetime:
    """Convert an RFC3339 formatted string to a datetime."""
    return datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ").replace(
        tzinfo=timezone.utc
    )


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


async def async_create_kernel(kernel_name: str):
    logging.info(f"Starting kernel for spec '{kernel_name}'")

    km = AsyncKernelManager(kernel_name=kernel_name)
    await km.start_kernel()

    client: AsyncKernelClient = km.client()
    client.start_channels()

    await client.wait_for_ready()

    logging.info("Kernel started")

    return km, client


msg_id_to_queue: dict[str, Queue] = {}


async def async_msg_producer(km: AsyncKernelManager, kc: AsyncKernelClient):
    try:
        while True:
            logging.info("Waiting for message...")

            msg = await kc.get_iopub_msg()

            log_jupyter_kernel_message(msg)

            parent_msg_id = msg["parent_header"].get("msg_id")
            if parent_msg_id in msg_id_to_queue:
                await msg_id_to_queue[parent_msg_id].put(msg)

    except Exception as e:
        logging.error(f"Error in message producer: {e}")
        await async_shutdown(km)


async def async_shutdown(km: AsyncKernelManager):
    logging.info("Shutting down kernel...")
    await km.shutdown_kernel()
    logging.info("Kernel shut down")
    sys.exit(0)


class State:
    def __init__(self, kernel_client: AsyncKernelClient):
        self.last_activity = datetime.now()
        self.kernel_client = kernel_client

    def reset_last_activity(self):
        self.last_activity = datetime.now()


class MainHandler(tornado.web.RequestHandler):
    def initialize(self, state: State):
        self.state = state

    async def get(self):
        try:
            is_alive = await client.is_alive()
            if not is_alive:
                raise Exception("kernel is not alive")
            self.write(
                PingResponse(
                    last_activity=datetime_to_rfc3339(self.state.last_activity)
                ).model_dump_json()
            )
        except Exception as e:
            self.set_status(500)
            self.write(Error(error=str(e)).model_dump_json())
            return


def serializer(o):
    if isinstance(o, datetime):
        return o.isoformat()
    raise TypeError("Type not serializable")


def log_jupyter_kernel_message(msg):
    m = json.dumps(msg, default=serializer)
    logging.info(f"Jupyter: {m}")


class ExecuteHandler(tornado.web.RequestHandler):
    def initialize(self, state: State):
        self.state = state

    async def post(self):
        parent_msg_id = None
        res: ExecuteResponse = ExecuteResponse(status=ExecutionStatusOK, events=[])

        try:
            logging.info(f"Execute request: {self.request.body}")
            self.state.reset_last_activity()

            req = ExecuteRequest.model_validate_json(self.request.body)

            local_queue = Queue()
            parent_msg_id = self.state.kernel_client.execute(req.code)
            msg_id_to_queue[parent_msg_id] = local_queue

            # Use the timeout logic on message processing
            try:
                await asyncio.wait_for(
                    self.process_messages(parent_msg_id, local_queue, res),
                    timeout=req.timeout_secs,
                )
            except asyncio.TimeoutError:
                logging.info(f"Timeout after {req.timeout_secs}s")
                res.status = ExecutionStatusTimeout
                return self.write(res.model_dump_json())

            self.state.reset_last_activity()
            self.write(res.model_dump_json())

        except Exception as e:
            self.set_status(500)
            self.write(Error(error=str(e)).model_dump_json())

        finally:
            # Cleanup after processing all messages
            if parent_msg_id is not None and parent_msg_id in msg_id_to_queue:
                del msg_id_to_queue[parent_msg_id]

            logging.info(f"Execute response: {res.model_dump_json()}")

    async def process_messages(self, parent_msg_id, queue, res):
        while True:
            msg = await queue.get()

            if msg["msg_type"] not in JupyterSupportedMessageTypes:
                continue

            elif msg["msg_type"] == JupyterMessageTypeStatus:
                if msg["content"]["execution_state"] == JupyterExecutionStateIdle:
                    break

            elif msg["msg_type"] == JupyterMessageTypeStream:
                res.events.append(
                    ExecutionEvent(
                        type=ExecutionEventTypeStream,
                        timestamp=datetime_to_rfc3339(datetime.now()),
                        data=ExecutionEventStream(
                            stream=msg["content"]["name"],
                            text=msg["content"]["text"],
                        ),
                    )
                )

            elif msg["msg_type"] == JupyterMessageTypeDisplayData:
                res.events.append(
                    ExecutionEvent(
                        type=ExecutionEventTypeDisplayData,
                        timestamp=datetime_to_rfc3339(datetime.now()),
                        data=ExecutionEventDisplayData(variants=msg["content"]["data"]),
                    )
                )

            elif msg["msg_type"] == JupyterMessageTypeError:
                res.events.append(
                    ExecutionEvent(
                        type=ExecutionEventTypeError,
                        timestamp=datetime_to_rfc3339(datetime.now()),
                        data=ExecutionEventError(
                            ename=msg["content"]["ename"],
                            evalue=msg["content"]["evalue"],
                            traceback=msg["content"]["traceback"],
                        ),
                    )
                )

            elif msg["msg_type"] == JupyterMessageTypeExecuteResult:
                res.events.append(
                    ExecutionEvent(
                        type=ExecutionEventTypeDisplayData,
                        timestamp=datetime_to_rfc3339(datetime.now()),
                        data=ExecutionEventDisplayData(variants=msg["content"]["data"]),
                    )
                )


@tornado.web.stream_request_body
class FileUploadHandler(tornado.web.RequestHandler):
    def initialize(self, state: State):
        self.state = state
        self.file_obj = None

    async def prepare(self):
        if self.request.method != "POST":
            self.set_status(404)
            self.finish()
            return

        path = self.path_args[0]
        full_path = os.path.join("/", path)

        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        self.file_obj = open(full_path, "wb")

        content_length = int(self.request.headers.get("Content-Length", 0))
        logging.info(f"File upload: '{path}' (Content-Length: {content_length})")

    def data_received(self, chunk):
        if self.file_obj:
            self.file_obj.write(chunk)

    async def post(self, path):
        self.state.reset_last_activity()
        if self.file_obj:
            self.file_obj.close()
        self.set_status(201)


class FileDownloadHandler(tornado.web.RequestHandler):
    def initialize(self, state: State):
        self.state = state

    async def get(self, path):
        self.state.reset_last_activity()

        full_path = os.path.join("/", path)

        if not os.path.exists(full_path):
            self.set_status(404)
            self.write(Error(error="file not found").model_dump_json())
            return

        content_length = os.path.getsize(full_path)
        logging.info(f"File download: '{path}' (Content-Length: {content_length})")

        # Set appropriate headers for file download
        self.set_header("Content-Length", content_length)
        self.set_header("Content-Type", "application/octet-stream")
        self.set_header(
            "Content-Disposition",
            f"attachment; filename*=UTF-8''{tornado.escape.url_escape(os.path.basename(full_path))}",
        )

        # Stream the file to the client
        with open(full_path, "rb") as f:
            while True:
                chunk = f.read(64 * 1024)
                if not chunk:
                    break
                try:
                    self.write(chunk)
                    await self.flush()
                except tornado.iostream.StreamClosedError:
                    return


def shutdown(ioloop: tornado.ioloop.IOLoop, km):
    logging.info("Shutting down server...")
    ioloop.add_callback_from_signal(lambda: async_shutdown(km))


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--port", type=int, default=80)
    p.add_argument("--kernel-name", type=str, default="python3")
    args = p.parse_args()

    km, client = asyncio.run(async_create_kernel(args.kernel_name))

    state = State(client)

    application = tornado.web.Application(
        [
            (r"/", MainHandler, {"state": state}),
            (r"/execute", ExecuteHandler, {"state": state}),
            (r"/files/upload/-/(.*)", FileUploadHandler, {"state": state}),
            (r"/files/download/-/(.*)", FileDownloadHandler, {"state": state}),
        ]
    )

    application.listen(args.port)

    logging.info(f"Server started at http://localhost:{args.port}")

    ioloop = tornado.ioloop.IOLoop.current()

    signal.signal(signal.SIGINT, lambda sig, frame: shutdown(ioloop, km))
    signal.signal(signal.SIGTERM, lambda sig, frame: shutdown(ioloop, km))

    ioloop.add_callback(async_msg_producer, km, client)

    tornado.ioloop.IOLoop.current().start()
