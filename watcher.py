# Подготовка чистой версии watcher.py без ApplicationBuilder
clean_watcher_code = """import requests
from bs4 import BeautifulSoup
import json
import time
import os
from telegram import Bot

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)

DATA_FILE = "storage/data.json"
CACHE_DIR = "storage/following_cache"

if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def get_following(user):
    try:
        url = f"https://whotwi.com/{user}/following"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        return sorted(set(a.text.strip("@") for a in soup.select("div.user-name a")))
    except Exception as e:
        print(f"[!] Failed to fetch for @{user}: {e}")
        return []

def load_previous(user):
    path = os.path.join(CACHE_DIR, f"{user}.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return []

def save_current(user, following):
    path = os.path.join(CACHE_DIR, f"{user}.json")
    with open(path, "w") as f:
        json.dump(following, f)

def check_updates():
    data = load_data()
    for chat_id, usernames in data.items():
        for username in usernames:
            print(f"🔍 Checking @{username} for chat {chat_id}")
            current = get_following(username)
            previous = load_previous(username)
            if not current:
                continue

            added = sorted(set(current) - set(previous))
            removed = sorted(set(previous) - set(current))

            if added or removed:
                message = f"📡 Изменения в подписках @{username}:"
                if added:
                    message += "\\n➕ Подписался на:\\n" + "\\n".join(f"@{u}" for u in added)
                if removed:
                    message += "\\n➖ Отписался от:\\n" + "\\n".join(f"@{u}" for u in removed)
                bot.send_message(chat_id=chat_id, text=message)

            save_current(username, current)

if __name__ == "__main__":
    print("👁️ Watcher запущен. Проверка каждые 30 секунд...")
    while True:
        check_updates()
        time.sleep(30)
"""

clean_watcher_path = "/mnt/data/watcher.py"
with open(clean_watcher_path, "w") as f:
    f.write(clean_watcher_code)
