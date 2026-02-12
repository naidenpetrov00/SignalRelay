from fastapi import FastAPI, HTTPException, Query, Request
from datetime import datetime
import os
import logging
from typing import Union

from dotenv import load_dotenv

from models.signal import SignalType, TvSignal, SignalPayload
from services.orders.helpers import classify_signal
from services.storage import append_signal
from config import FILE_PATH

load_dotenv()

app = FastAPI()
logger = logging.getLogger("signalrelay")
SECRET = os.getenv("SIGNAL_RELAY_SECRET")
if not SECRET:
    raise RuntimeError("SIGNAL_RELAY_SECRET is not set")


@app.post("/VWAP5m")
def tv_webhook(
    signal: Union[TvSignal, SignalPayload],
    request: Request,
    key: str = Query(..., description="App secret"),
):
    logger.info("Request:%s", request)

    if key != SECRET:
        logger.warning(
            "tv_webhook unauthorized: ip=%s symbol=%s",
            request.client.host if request.client else "unknown",
        )
        raise HTTPException(status_code=401, detail="unauthorized")
    signal_type = classify_signal(signal)

    append_signal(FILE_PATH, data)

    return {"status": "ok", "written": data}
