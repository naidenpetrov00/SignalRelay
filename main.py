from fastapi import FastAPI, Request, HTTPException
from datetime import datetime
import json
import os

from pydantic import BaseModel

app = FastAPI()

FILE_PATH = (
    r"C:\Users\naide\AppData\Roaming\MetaQuotes\Terminal\Common\Files\signals.jsonl"
)
# FILE_PATH = "/home/naidenpetrov00/.mt5/drive_c/users/naidenpetrov00/AppData/Roaming/MetaQuotes/Terminal/Common/Files/signals.jsonl"

REQUIRED_FIELDS = {"symbol", "action", "volume"}


def is_valid_signal(data: dict) -> bool:
    return REQUIRED_FIELDS.issubset(data.keys())


class TvSignal(BaseModel):
    symbol: str
    action: str
    volume: float
    stoploss: float


@app.post("/tv-webhook")
async def tv_webhook(signal: TvSignal):
    data = {
        "id": int(datetime.now().timestamp()),
        "symbol": signal.symbol,
        "action": signal.action,
        "volume": signal.volume,
        "stoploss": signal.stoploss,
    }

    os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)

    with open(FILE_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(data) + "\n")

    return {"status": "ok", "written": data}
