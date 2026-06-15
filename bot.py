from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import google.generativeai as genai
import os
from flask import Flask
from threading import Thread

# ═══════════════════════════════════════
# الإعدادات
# ═══════════════════════════════════════
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
BOT_PERSONALITY = "أنت مساعد ودي. رد باختصار وبالعربي."

# ═══════════════════════════════════════
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
chat_history = {}

# Flask app عشان Render
app_flask = Flask(__name__)

@app_flask.route('/')
def home():
    return "🤖 البوت شغال!"

def run_flask():
    app_flask.run(host='0.0.0.0', port=10000)

# ═══════════════════════════════════════
# البوت
# ═══════════════════════════════════════
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
    # شغل Flask في thread منفصل
    Thread(target=run_flask).start()
    
    # شغل البوت
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, smart_reply))
    
    print("🤖 البوت شغال 24/7!")
    application.run_polling()

if __name__ == "__main__":
    main()
