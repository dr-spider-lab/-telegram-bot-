from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import google.generativeai as genai
import os

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
BOT_PERSONALITY = "أنت مساعد ودي. رد باختصار وبالعربي."

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
chat_history = {}

async def smart_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_message = update.message.text
    
    if user_id not in chat_history:
        chat_history[user_id] = model.start_chat(history=[])
        chat_history[user_id].send_message(BOT_PERSONALITY)
    
    try:
        response = chat_history[user_id].send_message(user_message)
        await update.message.reply_text(response.text)
    except:
        await update.message.reply_text("عذراً، حدث خطأ!")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, smart_reply))
    print("🤖 البوت شغال 24/7!")
    app.run_polling()

if __name__ == "__main__":
    main()
