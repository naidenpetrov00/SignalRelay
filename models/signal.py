from enum import Enum
from typing import Optional, Union
from pydantic import BaseModel, Field, field_validator, model_validator, validator
import json

class TvSignal(BaseModel):
    symbol: str
    action: str
    volume: float
    stoploss: float

class SignalType(str, Enum):
    READY = "READY"
    EXECUTE = "EXECUTE"
    CLOSE = "CLOSE"

class OrderId(Enum):
    BUY = "BUY"
    SELL = "SELL"
    TP = "Close entry(s) order strategy.close"
    SL = "SL"
    EXIT_SHORT = "Exit Short"


class OrderType(Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"


class CommentData(BaseModel):
    leverage: float = 0
    order_type: OrderType = OrderType.LIMIT
    sl: float | None = None
    tp: float | None = None
    limit_price: float | None = None


class Bar(BaseModel):
    time: str
    open: float
    high: float
    low: float
    close: float
    volume: float


class Strategy(BaseModel):
    position_size: float
    order_action: str
    order_contracts: float
    order_price: float
    order_id: OrderId | str
    market_position: str
    market_position_size: float
    prev_market_position: str
    prev_market_position_size: float

    @field_validator("order_id", mode="before")
    def normalize_order_id(cls, v):
        if isinstance(v, str):
            if v.startswith(OrderId.TP.value):
                return OrderId.TP
        return v


class SignalPayload(BaseModel):
    strategyName: str
    order_type: str
    time: str
    exchange: str
    timeframe: str
    ticker: str
    leverage: str
    comment: str
    bar: Bar
    strategy: Strategy
    passphrase: Optional[str] = ""

    comment_data: CommentData = Field(default_factory=CommentData)

    @model_validator(mode="before")
    def pase_comment_json(cls, model: dict):
        comment = model.get("comment")
        if comment == "SLFromTV":
            model["comment_data"] = CommentData()
            return model
        elif comment:
            try:
                parsed = json.loads(comment)
                if isinstance(parsed, dict):
                    model["comment_data"] = CommentData(**parsed)
            except Exception:
                print("Not Json")
        return model
