import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running!")

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    server.serve_forever()

Thread(target=run_web_server, daemon=True).start()
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import google.generativeai as genai
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    try:
        response = model.generate_content(user_message)
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text("ይቅርታ፣ ጥያቄዎን በሚሰራበት ጊዜ ችግር አጋጥሟል።")

if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)
    application.add_handler(message_handler)
    print("ቦቱ በመሥራት ላይ ነው...")
        PORT = int(os.environ.get("PORT", 10000))
    RENDER_URL = "https://telegram-bot-1-i0ta.onrender.com"
    
    application.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        drop_pending_updates=True,
        webhook_url=f"{RENDER_URL}/"
)

