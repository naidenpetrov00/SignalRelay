from enum import Enum
from typing import Union, Tuple
import logging

from models.signal import OrderId, SignalPayload, SignalType, TvSignal

logger = logging.getLogger("signalrelay.classify_signal")


def classify_signal(payload: Union[TvSignal, SignalPayload]) -> Tuple[SignalType, Union[TvSignal, SignalPayload]]:
    symbol = getattr(payload, "symbol", getattr(payload, "ticker", None))

    if isinstance(payload, TvSignal):
        logger.info("classify_signal: type=TvSignal symbol=%s result=%s", symbol, SignalType.READY.value)
        return SignalType.READY, payload
    elif isinstance(payload, SignalPayload):
        order_id = payload.strategy.order_id
        if order_id == OrderId.TP or order_id == OrderId.TP.value:
            logger.info(
                "classify_signal: type=SignalPayload symbol=%s order_id=%s result=%s",
                symbol,
                order_id,
                SignalType.CLOSE.value
            )
            return SignalType.CLOSE, payload
        elif payload.comment_data.tp or payload.comment_data.sl:
            logger.info(
                "classify_signal: type=SignalPayload symbol=%s tp=%s sl=%s result=%s",
                symbol,
                bool(payload.comment_data.tp),
                bool(payload.comment_data.sl),
                SignalType.EXECUTE.value,
            )
            return SignalType.EXECUTE, payload
    logger.info("classify_signal: type=unknown symbol=%s result=%s", symbol, SignalType.READY.value)
    return SignalType.READY, payload
