import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import google.generativeai as genai

# ሎግንግ ማስተካከል
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ቁልፎችን ከ Environment Variables ማንበብ
BOT_TOKEN = os.environ.get("BOT_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# ጂሚኒን ማዋቀር
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    try:
        response = model.generate_content(user_message)
        await update.message.reply_text(response.text)
    except Exception as e:
        logger.error(f"ስህተት አጋጥሟል: {e}")
        await update.message.reply_text("ይቅርታ፣ ስህተት አጋጥሟል። እባክዎ እንደገና ይሞክሩ።")

def main():
    # ቦቱን መገንባት
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # የመልእክት ሃንድለር መጨመር
    message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)
    application.add_handler(message_handler)

    # የ Render ዌብሁክ ማዋቀሪያ
    PORT = int(os.environ.get("PORT", 10000))
    RENDER_URL = "https://telegram-bot-1-i0ta.onrender.com"

    print("ቦቱ በዌብሁክ (Webhook) በመሠራት ላይ ነው...")
    application.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        drop_pending_updates=True,
        webhook_url=f"{RENDER_URL}/"
    )

if __name__ == '__main__':
    main()
