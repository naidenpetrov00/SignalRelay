import os

# DEFAULT_SIGNAL_PATH = (
#     r"C:\Users\naide\AppData\Roaming\MetaQuotes\Terminal\Common\Files\signals.jsonl"
# )
DEFAULT_SIGNAL_PATH = "/home/naidenpetrov00/.mt5/drive_c/users/naidenpetrov00/AppData/Roaming/MetaQuotes/Terminal/Common/Files/signals.jsonl"

FILE_PATH = os.getenv("SIGNAL_FILE_PATH", DEFAULT_SIGNAL_PATH)
