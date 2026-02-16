from fastapi import FastAPI, HTTPException, Query, Request
import os
import logging

from dotenv import load_dotenv

from models.signal import TvSignal
from services.orders.signal_distributor import signal_distributor

load_dotenv()

app = FastAPI()
logger = logging.getLogger("signalrelay")
SECRET = os.getenv("SIGNAL_RELAY_SECRET")
if not SECRET:
    raise RuntimeError("SIGNAL_RELAY_SECRET is not set")


@app.post("/VWAP5m")
def tv_webhook(
    signal: TvSignal,
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

    data = signal_distributor(signal)

    return {"status": "ok", "written": data}
