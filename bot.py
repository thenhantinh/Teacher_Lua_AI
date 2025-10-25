import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import openai

# Cấu hình
TELEGRAM_BOT_TOKEN = "7673124677:AAHi0GxG8xkEjBGZQBB22JHXdJwqudkOj9o"
OPENAI_API_KEY = "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"

# Khởi tạo OpenAI
openai.api_key = OPENAI_API_KEY

# Thiết lập logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Hàm xử lý tin nhắn AI
async def generate_ai_response(message_text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Bạn là một trợ lý AI hữu ích."},
                {"role": "user", "content": message_text}
            ],
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Xin lỗi, tôi gặp sự cố: {str(e)}"

# Command handlers
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Xin chào! Tôi là trợ lý AI. Hãy chat với tôi!"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
Các lệnh có sẵn:
/start - Bắt đầu
/help - Trợ giúp
/info - Thông tin về bot
    """
    await update.message.reply_text(help_text)

# Xử lý tin nhắn
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type = update.message.chat.type
    text = update.message.text

    # Chỉ phản hồi trong nhóm khi được đề cập hoặc tin nhắn riêng
    if message_type == 'group' or message_type == 'supergroup':
        if context.bot.username in text or update.message.reply_to_message and update.message.reply_to_message.from_user.id == context.bot.id:
            # Loại bỏ username khỏi tin nhắn
            if context.bot.username in text:
                text = text.replace(f"@{context.bot.username}", "").strip()
            
            # Tạo phản hồi AI
            response = await generate_ai_response(text)
            await update.message.reply_text(response)
    else:  # Tin nhắn riêng
        response = await generate_ai_response(text)
        await update.message.reply_text(response)

# Xử lý lỗi
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.error(f"Update {update} caused error {context.error}")

# Hàm chính
def main():
    # Tạo ứng dụng
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Thêm handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Xử lý lỗi
    app.add_error_handler(error)

    # Khởi động bot
    print("Bot đang chạy...")
    app.run_polling(poll_interval=3)

if __name__ == "__main__":
    main()from telegram import Update
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
