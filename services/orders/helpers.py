from enum import Enum
from typing import Union

from models.signal import OrderId, SignalPayload, SignalType, TvSignal



def classify_signal(payload: Union[TvSignal, SignalPayload]) -> SignalType:
    if isinstance(payload, TvSignal):
        return SignalType.READY
    elif isinstance(payload, SignalPayload):
        if payload.strategy.order_id == OrderId.TP:
            return SignalType.CLOSE
        elif payload.comment_data.tp or payload.comment_data.sl:
            return SignalType.EXECUTE
    return SignalType.READY
