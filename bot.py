from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from openai import OpenAI

# --- Thông tin cấu hình ---
TELEGRAM_TOKEN = "7673124677:AAHi0GxG8xkEjBGZQBB22JHXdJwqudkOj9o"
OPENAI_API_KEY = "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"

client = OpenAI(api_key=OPENAI_API_KEY)

# --- Hàm xử lý tin nhắn ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    chat_id = update.message.chat_id

    # Gửi yêu cầu đến OpenAI
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # hoặc "gpt-4", "gpt-5" khi có
        messages=[
            {"role": "system", "content": "Bạn là trợ lý AI thông minh, nói chuyện tự nhiên và thân thiện."},
            {"role": "user", "content": user_message}
        ]
    )

    answer = response.choices[0].message.content
    await update.message.reply_text(answer)

# --- Chạy bot ---
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
print("🤖 Bot đang chạy...")
app.run_polling()
