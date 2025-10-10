from fastapi import FastAPI, HTTPException
from fastapi.requests import Request
from .models import BaseTelemetry, AndroidTelemetry
from .db import get_conn
import time, json

app = FastAPI()

@app.post('/collect')
async def collect(req: Request):
    payload = await req.json()
    if 'type' not in payload or 'device_id' not in payload:
        raise HTTPException(status_code=400, detail="type and device_id required")


    t = payload.get('type')
    try:
        if t == 'android':
            obj = AndroidTelemetry(**payload)
        else:
            obj = BaseTelemetry(**payload)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"invalid payload: {e}")

    now = payload.get('timestamp', time.time())
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(
        'INSERT INTO telemetry (timestamp, type, device_id, data) VALUES (?, ?, ?, ?)',
        (now, obj.type, obj.device_id, json.dumps(obj.model_dump()))
        )
        conn.commit()

    return {"status": "ok"}


@app.get('/health')
def health():
    return {"status": "ok"}

@app.get('/')
def root():
    return {"message": "HELO"}