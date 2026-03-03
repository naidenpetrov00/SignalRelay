from datetime import datetime, timezone
import logging

from config import DEFAULT_READY_SIGNAL_PATH, DEFAULT_TP_READY_SIGNAL_PATH
from models.signal import SignalPayload, SignalType, TvSignal
from services.orders.helpers import classify_signal
from services.storage import append_signal

logger = logging.getLogger("signalrelay.signal_distributor")


def _timestamp_id() -> int:
    return int(datetime.now(timezone.utc).timestamp() * 1000)


def _build_ready_record(signal: TvSignal) -> dict:
    return {
        "id": _timestamp_id(),
        "type": SignalType.READY.value,
        "received_at": datetime.now(timezone.utc).isoformat(),
        "symbol": signal.symbol,
        "action": signal.action,
        "crossedPrice": signal.crossedPrice,
        "stoploss": signal.stoploss,
        "stoploss": signal.tpType,
    }


def _build_tp_ready_record(signal: TvSignal) -> dict:
    return {
        "id": _timestamp_id(),
        "type": SignalType.TPREADY.value,
        "received_at": datetime.now(timezone.utc).isoformat(),
        "symbol": signal.symbol,
        "action": signal.action,
        "closePart": signal.closePart,
    }


def _build_execute_record(signal: SignalPayload) -> dict:
    return {
        "id": _timestamp_id(),
        "type": SignalType.EXECUTE.value,
        "received_at": datetime.now(timezone.utc).isoformat(),
        "strategy_name": signal.strategyName,
        "ticker": signal.ticker,
        "order_action": signal.strategy.order_action,
        "order_id": str(signal.strategy.order_id),
        "order_price": signal.strategy.order_price,
        "tp": signal.comment_data.tp,
        "sl": signal.comment_data.sl,
        "limit_price": signal.comment_data.limit_price,
        "raw": signal.model_dump(mode="json"),
    }


def _build_close_record(signal: SignalPayload) -> dict:
    return {
        "id": _timestamp_id(),
        "type": SignalType.CLOSE.value,
        "received_at": datetime.now(timezone.utc).isoformat(),
        "strategy_name": signal.strategyName,
        "ticker": signal.ticker,
        "order_action": signal.strategy.order_action,
        "order_id": str(signal.strategy.order_id),
        "market_position": signal.strategy.market_position,
        "raw": signal.model_dump(mode="json"),
    }


def signal_distributor(signal: TvSignal) -> dict:
    signal_type = classify_signal(signal)

    if signal_type == SignalType.READY:
        if not isinstance(signal, TvSignal):
            raise TypeError("SignalType.READY expects TvSignal payload")
        record = _build_ready_record(signal)
        append_signal(DEFAULT_READY_SIGNAL_PATH, record)
    elif signal_type == SignalType.TPREADY:
        record = _build_tp_ready_record(signal)
        append_signal(DEFAULT_TP_READY_SIGNAL_PATH, record)
    else:
        raise ValueError(f"Unsupported signal type: {signal_type}")

    logger.info(
        "signal_distributor: type=%s symbol=%s",
        record["type"],
        record.get("symbol", record.get("ticker", "unknown")),
    )
    return record
