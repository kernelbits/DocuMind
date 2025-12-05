import json 
from datetime import datetime 
import os 

folder = "./logs"
file_path = "./logs/chat_logs.json"

if not os.path.exists(folder):
    os.mkdirs(folder)
if not os.path.exists(file_path):
    with open(file_path,"w") as f:
        f.write("")


def save_log_chat(user_message:str, bot_message:str):
    timestamp = datetime.now()
    timestamp_formatted = timestamp.strftime("%Y-%m-%d %H:%M:%S")
    data = {
        'user':user_message,
        'bot':bot_message,
        'timestamp':timestamp_formatted
    }
    with open("./logs/chat_logs.json","a") as f:
        json.dump(data,f,indent=3)
        f.write("\n")