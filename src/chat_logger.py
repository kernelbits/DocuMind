import json
from datetime import datetime
import os

folder = "./logs"
file_path = "./logs/chat_logs.json"

# Ensure logs folder exists
os.makedirs(folder, exist_ok=True)

# Ensure file exists
if not os.path.exists(file_path):
    open(file_path, "a", encoding="utf-8").close()

def save_log_chat(user_message: str, bot_message: str):
    """
    Append a single compact JSON object per line (JSONL).
    Keeps logging simple and avoids crashes on write errors.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = {"user": user_message, "bot": bot_message, "timestamp": timestamp}
    try:
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(data, ensure_ascii=False) + "\n")
    except Exception as e:
        # Non-fatal for MVP: print error so you can see it in logs
        print(f"[chat_logger] Failed to write log: {e}")