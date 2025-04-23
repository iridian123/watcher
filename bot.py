import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import json
import os

DATA_FILE = "storage/data.json"

logging.basicConfig(level=logging.INFO)

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Привет! Отправь /add @username чтобы следить за аккаунтом в X.")

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Укажи username после команды, например: /add @elonmusk")
        return

    username = context.args[0].lstrip("@")
    user_id = str(update.effective_user.id)

    data = load_data()
    if user_id not in data:
        data[user_id] = []
    if username not in data[user_id]:
        data[user_id].append(username)
        save_data(data)
        await update.message.reply_text(f"✅ Теперь слежу за @{username}")
    else:
        await update.message.reply_text("⚠️ Ты уже следишь за этим аккаунтом.")

async def remove(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Укажи username после команды, например: /remove @elonmusk")
        return

    username = context.args[0].lstrip("@")
    user_id = str(update.effective_user.id)

    data = load_data()
    if user_id in data and username in data[user_id]:
        data[user_id].remove(username)
        save_data(data)
        await update.message.reply_text(f"🗑️ Больше не слежу за @{username}")
    else:
        await update.message.reply_text("🤔 Ты не следил за этим аккаунтом.")

async def list_following(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    data = load_data()
    if user_id in data and data[user_id]:
        accounts = "\n".join([f"@{u}" for u in data[user_id]])
await update.message.reply_text(f"📋 Ты следишь за:\n{accounts}")
{accounts}")
    else:
        await update.message.reply_text("Ты пока ни за кем не следишь.")

def main():
    import os
    TOKEN = os.getenv("BOT_TOKEN")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add", add))
    app.add_handler(CommandHandler("remove", remove))
    app.add_handler(CommandHandler("list", list_following))
    app.run_polling()

if __name__ == "__main__":
    main()
