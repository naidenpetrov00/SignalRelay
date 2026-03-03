import os

# DEFAULT_SIGNAL_PATH = (
#     r"C:\Users\naide\AppData\Roaming\MetaQuotes\Terminal\Common\Files\signals.jsonl"
# )
DEFAULT_READY_SIGNAL_PATH = "/home/naidenpetrov00/.mt5/drive_c/users/naidenpetrov00/AppData/Roaming/MetaQuotes/Terminal/Common/Files/signals.jsonl"
DEFAULT_TP_READY_SIGNAL_PATH = "/home/naidenpetrov00/.mt5/drive_c/users/naidenpetrov00/AppData/Roaming/MetaQuotes/Terminal/Common/Files/tp_signals.jsonl"

DEFAULT_READY_SIGNAL_PATH = os.getenv("SIGNAL_FILE_PATH", DEFAULT_READY_SIGNAL_PATH)
DEFAULT_TP_READY_SIGNAL_PATH = os.getenv("SIGNAL_FILE_PATH", DEFAULT_TP_READY_SIGNAL_PATH)
