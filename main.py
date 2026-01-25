from fastapi import FastAPI
from datetime import datetime
import json
import os
from typing import Union

from models.signal import SignalType, TvSignal, SignalPayload
from services.orders.helpers import classify_signal
from services.storage import append_signal
from config import FILE_PATH

app = FastAPI()

@app.post("/VWAP5m")
def tv_webhook(signal: Union[TvSignal, SignalPayload]):
    # Determine type
    signal_type = classify_signal(signal)

    # Convert to dict for storage
    data = {
        "id": int(datetime.now().timestamp()),
        "symbol": getattr(signal, "symbol", getattr(signal, "ticker", None)),
        "action": "CLOSE" if signal_type == SignalType.CLOSE else getattr(signal, "action", None),
        "volume": getattr(signal, "volume", 0),
        "stoploss": getattr(signal, "stoploss", None),
        "type": signal_type.value
    }

    append_signal(FILE_PATH, data)

    return {"status": "ok", "written": data}
