# Sandbox API

### Ping

**Path:** GET `/`

Check whether a sandbox is alive and return information about it.

#### Request

-

#### Response

**Status:**
- `200` if alive

**Example:**

```json
{
    "last_activity": "2006-01-02T15:04:05Z07:00", // RFC 3339
}
```

### Execute

**Path:** POST `/execute`

#### Request

**Content-Type:** `application/json`

**JSON Schema:**

| Name           | Type              | Description                                                                                            |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------ |
| `code`         | string            | The code to be executed.                                                                               |
| `timeout_secs` | number (Optional) | Abort execution after timeout. Does not include environment and runtime creation time. Defaults to 60. |

#### Response

**Status:**
- `200` if successful

**Content-Type:** `application/json`

**Example:**

```json
{
    "status": "ok", // Possible values: "ok", "timeout"
    "events": [
        {
            "type": "stream",
            "timestamp": "2006-01-02T15:04:05Z07:00", // RFC 3339
            "data": {
                "name": "stdout", // Possible values: "stdout", "stderr"
                "text": "Hello World!",
            }
        },
        {
            "type": "display_data",
            "timestamp": "2006-01-02T15:04:05Z07:00", // RFC 3339
            "data": {
                "variants": {
                    "text/plain": "<IPython.core.display.Image object>",
                    "image/png": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADElEQVR4nGP4//8/AAX+Av4N70a4AAAAAElFTkSuQmCC" // Base64 encoded PNG image
                }
            }
        },
        {
            "type": "file", // The program has written a file to disk.
            "timestamp": "2006-01-02T15:04:05Z07:00", // RFC 3339
            "data": {
                "path": "README.md",
                "size": 128, // Size is expressed in bytes
            }
        },
        {
            "type": "error",
            "timestamp": "2006-01-02T15:04:05Z07:00", // RFC 3339
            "data": {
                "ename": "ZeroDivisionError",
                "evalue": "division by zero",
                "traceback": [
                    "\\u001b[0;31m---------------------------------------------------------------------------\\u001b[0m",
                    "\\u001b[0;31mZeroDivisionError\\u001b[0m                         Traceback (most recent call last)",
                    "Cell \\u001b[0;32mIn[1], line 2\\u001b[0m\\n\\u001b[1;32m      1\\u001b[0m \\u001b[38;5;66;03m# \\u8ba1\\u7b97\\u8868\\u8fbe\\u5f0f\\u7684\\u7ed3\\u679c\\u001b[39;00m\\n\\u001b[0;32m----> 2\\u001b[0m result \\u001b[38;5;241m=\\u001b[39m \\u001b[38;5;241;43m361234\\u001b[39;49m\\u001b[43m \\u001b[49m\\u001b[38;5;241;43m/\\u001b[39;49m\\u001b[43m \\u001b[49m\\u001b[38;5;241;43m0\\u001b[39;49m \\u001b[38;5;241m+\\u001b[39m \\u001b[38;5;241m4514\\u001b[39m \\u001b[38;5;241m*\\u001b[39m \\u001b[38;5;241m1234\\u001b[39m \\u001b[38;5;241m-\\u001b[39m \\u001b[38;5;241m27152346\\u001b[39m \\u001b[38;5;241m/\\u001b[39m \\u001b[38;5;241m2023\\u001b[39m\\n\\u001b[1;32m      3\\u001b[0m result\\n",
                    "\\u001b[0;31mZeroDivisionError\\u001b[0m: division by zero"
                ]
            }
        }
    ]
}
```

### File upload

**Path:** POST `/files/upload/-/*path`

Upload a file to the sandbox under `*path`.

#### Request

**Content-Length:** The length of the file in bytes.

**Body:** The raw contents of the file as bytes.

#### Response

**Status:**
- `201` if upload was successful
- `409` if file already exists

### File download

**Path:** GET `/files/download/-/*path`

Download a file from the sandbox from `*path`.

#### Request

\-

#### Response

**Content-Type:** Automatically detected, depending on the file.

**Content-Disposition:** `attachment; filename*=UTF-8''<filename>`

**Body:** The raw contents of the file.

**Status:**
- `200` if file exists
- `404` if file is not found
