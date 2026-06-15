from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import os

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
BOT_PERSONALITY = "أنت مساعد ودي. رد باختصار وبالعربي."

# ردود جاهزة (بدل AI)
REPLIES = {
    "اهلا": "أهلاً بيك! 🌟",
    "مرحبا": "مرحباً! أنا بوت مساعد. هرد عليك في أقرب وقت! 🤖",
    "ازيك": "أنا كويس، شكراً! إنت عامل إيه؟",
    "hello": "Hello! I'm a bot assistant. I'll reply soon! 🤖",
    "hi": "Hi there! 👋",
}

async def smart_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text.lower().strip()
    
    # دور على رد جاهز
    for key, reply in REPLIES.items():
        if key in user_message:
            await update.message.reply_text(reply)
            return
    
    # لو مفيش رد جاهز
    await update.message.reply_text("شكراً لرسالتك! هرد عليك في أقرب وقت ممكن. ✅")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, smart_reply))
    print("🤖 البوت شغال!")
    app.run_polling()

if __name__ == "__main__":
    main()
