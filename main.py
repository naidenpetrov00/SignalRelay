from fastapi import FastAPI, HTTPException, Query, Request
from datetime import datetime
import json
import os
from typing import Union

from dotenv import load_dotenv

from models.signal import SignalType, TvSignal, SignalPayload
from services.orders.helpers import classify_signal
from services.storage import append_signal
from config import FILE_PATH

load_dotenv()

app = FastAPI()
SECRET = os.getenv("SIGNAL_RELAY_SECRET")
if not SECRET:
    raise RuntimeError("SIGNAL_RELAY_SECRET is not set")

@app.post("/VWAP5m")
def tv_webhook(
    signal: Union[TvSignal, SignalPayload],
    key: str = Query(..., description="App secret"),
):
    if key != SECRET:
        raise HTTPException(status_code=401, detail="unauthorized")
    signal_type = classify_signal(signal)
    data = {
        "id": int(datetime.now().timestamp()),
        "symbol": getattr(signal, "symbol", getattr(signal, "ticker", None)),
        "action": (
            "CLOSE"
            if signal_type == SignalType.CLOSE
            else getattr(signal, "action", None)
        ),
        "volume": getattr(signal, "volume", 0),
        "stoploss": getattr(signal, "stoploss", None),
        "type": signal_type.value,
    }

    append_signal(FILE_PATH, data)

    return {"status": "ok", "written": data}
