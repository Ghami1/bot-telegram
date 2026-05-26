import os
import logging
from fastapi import FastAPI, Request
import telegram
from telegram import Update
from telegram.ext import Application
import google.generativeai as genai

# 1. Konfigurasi (Gunakan environment variable untuk keamanan)
TELEGRAM_TOKEN = os.environ.get('8962005838:AAEJTzhSrMc61M9DPqCxxFqBwUvOxy-FS7g')
GEMINI_API_KEY = os.environ.get('AIzaSyDYqObZYJdUE2Mwr67a0aKc0vV2kImdu-I')

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. Setup Aplikasi
app = FastAPI()
bot = telegram.Bot(token=TELEGRAM_TOKEN)
application = Application.builder().token(TELEGRAM_TOKEN).build()

# 3. Fungsi AI
async def handle_message(update: Update, context):
    user_text = update.message.text
    # Mengirim ke Gemini
    response = model.generate_content(user_text)
    # Membalas ke Telegram
    await update.message.reply_text(response.text)

# Menambahkan handler (perintah /start dan pesan teks)
from telegram.ext import CommandHandler, MessageHandler, filters
application.add_handler(CommandHandler("start", lambda u, c: u.message.reply_text("Halo! Saya aktif.")))
application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

# 4. Webhook Endpoint
@app.post("/")
async def webhook(request: Request):
    json_data = await request.json()
    update = Update.de_json(json_data, bot)
    await application.process_update(update)
    return {"status": "ok"}
