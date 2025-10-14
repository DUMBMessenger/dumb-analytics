import json
import time

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.requests import Request

from shared import CERT_PEM, KEY_PEM
from .db import get_conn
from .models import BaseTelemetry, AndroidTelemetry, WebTelemetry
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/collect')
async def collect(req: Request):
    payload = await req.json()
    if 'type' not in payload or 'device_id' not in payload:
        raise HTTPException(status_code=400, detail="type and device_id required")


    t = payload.get('type')
    try:
        if t == 'android':
            obj = AndroidTelemetry(**payload)
        elif t == 'web':
            obj = WebTelemetry(**payload)
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

def main():
    if KEY_PEM.exists() and CERT_PEM.exists():
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=7634,
            ssl_keyfile=KEY_PEM,
            ssl_certfile=CERT_PEM
        )
    else:
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=7634
        )

if __name__ == '__main__':
    main()