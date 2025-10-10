# Dumb Analytics

**Dumb Analytics** — a simple tool for collecting and visualizing telemetry from PC and Android devices.
It consists of two parts: a **dashboard** (frontend) and an **API** for collecting data from clients.

---

## 🚀 Installation

1. Install Python (recommended 3.10+)
2. Clone the repository
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the main script:

```bash
python run_all.py
```

After running:

* Dashboard is available at port `7635`
* API for clients is available at port `7634`

---

## API Documentation

### 1. Health Check

**GET `/health`**

**Description:** Checks if the server is alive.

**Response:**

```json
{
  "status": "ok"
}
```

---

### 2. Collect Telemetry

**POST `/collect`**

**Description:** Receives telemetry from devices (PC or Android) and stores it in the database.

**Request Body (example for PC):**

```json
{
  "type": "pc",
  "device_id": "abc123",
  "timestamp": 1700000000,
  "os_name": "Windows",
  "os_version": "10",
  "kernel_version": "10.0.19044",
  "hostname": "my-pc",
  "uptime": 3600,
  "cpu": {
    "name": "Intel i5",
    "cores": 4,
    "threads": 8,
    "freq": 3.6
  },
  "ram": {
    "total": 16000,
    "used": 8000,
    "available": 8000
  },
  "disks": [
    {"mount": "C:", "total": 500000, "free": 200000}
  ],
  "gpu_name": "NVIDIA GTX 1060",
  "gpu_vram": 6144
}
```

**Request Body (example for Android):**

```json
{
  "type": "android",
  "device_id": "xyz789",
  "brand": "Samsung",
  "manufacturer": "Samsung",
  "android_version": "13",
  "sdk": 33,
  "battery_level": 85,
  "charging": true,
  "rooted": false,
  "storage": {"total": 128000, "free": 64000}
}
```

**Response:**

```json
{
  "status": "ok"
}
```

**Errors:**

* `400 Bad Request` — if required fields (`type` or `device_id`) are missing or the data is invalid.

---

### 3. Data Format

* `type`: `"pc"` or `"android"`
* `device_id`: unique device identifier
* Other fields are optional and depend on the device type.
* CPU, RAM, disk, and display fields follow the `CpuInfo`, `RamInfo`, `DiskEntry`, `DisplayInfo` models from `models.py`.

---

## Example Usage

Send telemetry from a client:

```python
import requests
import time

data = {
    "type": "pc",
    "device_id": "test-pc",
    "timestamp": time.time(),
    "os_name": "Linux",
    "cpu": {"name": "AMD Ryzen 5", "cores": 6, "threads": 12, "freq": 3.7}
}

res = requests.post("http://localhost:7634/collect", json=data)
print(res.json())
```

---

## Tips

* Open the dashboard at `7635` to view real-time statistics and graphs
* All data is stored in SQLite (file `DB_PATH`)