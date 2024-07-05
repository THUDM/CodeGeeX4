import os
import shutil
import tempfile
import unittest

import requests

from sandbox import (
    Error,
    ExecuteResponse,
    ExecutionEventTypeDisplayData,
    ExecutionEventTypeError,
    ExecutionEventTypeStream,
    ExecutionStatusOK,
    ExecutionStatusTimeout,
)

# We'll create a temporary directory for the tests to avoid any side effects.
temp_dir = tempfile.mkdtemp()

BASE_URL = "http://localhost:8888/"


def url(path: str) -> str:
    return BASE_URL + path


class TestExecuteHandler(unittest.TestCase):
    def must_bind_with_execute_response(self, r: requests.Response) -> ExecuteResponse:
        self.assertEqual(r.status_code, 200)
        return ExecuteResponse.model_validate_json(r.content)

    def must_bind_with_error(self, r: requests.Response) -> Error:
        return Error.model_validate_json(r.content)

    def test_execute_hello(self):
        r = requests.post(
            url("execute"), json={"code": "print('hello')", "timeout_secs": 10}
        )
        res = self.must_bind_with_execute_response(r)
        self.assertEqual(len(res.events), 1)
        self.assertEqual(res.events[0].type, ExecutionEventTypeStream)
        self.assertEqual(res.events[0].data.stream, "stdout")  # type: ignore
        self.assertEqual(res.events[0].data.text, "hello\n")  # type: ignore

    def test_execute_timeout(self):
        r = requests.post(
            url("execute"),
            json={"code": "import time\ntime.sleep(5)", "timeout_secs": 1},
        )
        res = self.must_bind_with_execute_response(r)
        self.assertEqual(len(res.events), 0)
        self.assertEqual(res.status, ExecutionStatusTimeout)

    def test_execute_syntax_error(self):
        r = requests.post(
            url("execute"), json={"code": "print('hello'", "timeout_secs": 10}
        )
        err = self.must_bind_with_execute_response(r)
        self.assertEqual(err.status, ExecutionStatusOK)
        self.assertEqual(len(err.events), 1)
        self.assertEqual(err.events[0].type, ExecutionEventTypeError)
        self.assertEqual(err.events[0].data.ename, "SyntaxError")  # type: ignore
        self.assertIsNotNone(err.events[0].data.evalue)  # type: ignore
        self.assertGreater(len(err.events[0].data.traceback), 0)  # type: ignore

    def test_execute_invalid_timeout(self):
        r = requests.post(
            url("execute"),
            json={"code": "print('hello')", "timeout_secs": -1},
        )
        self.must_bind_with_error(r)

    def test_execute_display_data(self):
        code = """import matplotlib.pyplot as plt
plt.plot([1, 2, 3, 4])
plt.ylabel('some numbers')
plt.show()"""

        r = requests.post(url("execute"), json={"code": code, "timeout_secs": 10})
        res = self.must_bind_with_execute_response(r)
        self.assertEqual(res.status, ExecutionStatusOK)
        self.assertEqual(len(res.events), 1)
        self.assertEqual(res.events[0].type, ExecutionEventTypeDisplayData)
        self.assertIsNotNone(res.events[0].data.variants["image/png"])  # type: ignore
        self.assertIsNotNone(res.events[0].data.variants["text/plain"])  # type: ignore

    def test_execute_pil_image(self):
        code = """from PIL import Image
img = Image.new('RGB', (60, 30), color = 'red')

# Override the show method of the Image class
def new_show(self, *args, **kwargs):
    display(self)

Image.Image.show = new_show

img.show()"""

        r = requests.post(url("execute"), json={"code": code, "timeout_secs": 10})
        res = self.must_bind_with_execute_response(r)
        self.assertEqual(res.status, ExecutionStatusOK)
        self.assertEqual(len(res.events), 1)
        self.assertEqual(res.events[0].type, ExecutionEventTypeDisplayData)
        self.assertIsNotNone(res.events[0].data.variants["image/png"])  # type: ignore
        self.assertIsNotNone(res.events[0].data.variants["text/plain"])  # type: ignore


class FileUploadHandlerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.mkdtemp()
        cls.BASE_URL = f"http://localhost:8888/files/upload/-{cls.temp_dir}/"

    def test_upload_file(self):
        file_path = os.path.join(self.temp_dir, "test.txt")

        large_binary_file = os.urandom(1024 * 1024 * 10)  # 10 MB

        r = requests.post(self.BASE_URL + "test.txt", data=large_binary_file)

        self.assertEqual(r.status_code, 201)
        self.assertTrue(os.path.exists(file_path))

        with open(file_path, "rb") as f:
            self.assertEqual(f.read(), large_binary_file)

    def test_upload_existing_file(self):
        file_path = os.path.join(self.temp_dir, "existing.txt")
        with open(file_path, "wb") as f:
            f.write(b"exists")

        with open(file_path, "rb") as f:
            r = requests.post(self.BASE_URL + "existing.txt", data=f.read())

        self.assertEqual(r.status_code, 409)
        error = Error.model_validate_json(r.content)
        self.assertEqual(error.error, "file already exists")

    def test_directory_creation(self):
        file_path = os.path.join(self.temp_dir, "newdir", "test.txt")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        r = requests.post(self.BASE_URL + "newdir/test.txt", data=b"test content")

        self.assertEqual(r.status_code, 201)
        self.assertTrue(os.path.exists(file_path))

        with open(file_path, "rb") as f:
            self.assertEqual(f.read(), b"test content")

    @classmethod
    def tearDownClass(cls):
        # Clean up the temp_dir after all tests
        if os.path.exists(cls.temp_dir):
            shutil.rmtree(cls.temp_dir)


if __name__ == "__main__":
    unittest.main()
