from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from openai import OpenAI
import os

TELEGRAM_TOKEN = os.getenv("7673124677:AAHi0GxG8xkEjBGZQBB22JHXdJwqudkOj9o")
OPENAI_API_KEY = os.getenv("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")

client = OpenAI(api_key=OPENAI_API_KEY)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Bạn là trợ lý AI thân thiện, trả lời tự nhiên."},
            {"role": "user", "content": user_message}
        ]
    )
    await update.message.reply_text(response.choices[0].message.content)

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("🤖 Bot đang chạy...")
app.run_polling()
