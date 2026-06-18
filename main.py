import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import google.generativeai as genai

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    system_instruction="Kamu adalah asisten pribadi yang helpful, ramah, dan selalu menjawab dalam Bahasa Indonesia."
)

histori = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Halo! Saya asisten AI pribadi kamu. Silakan ngobrol dengan saya!"
    )

async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    histori[user_id] = []
    await update.message.reply_text("Histori percakapan sudah dihapus!")

async def balas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    pesan_user = update.message.text

    if user_id not in histori:
        histori[user_id] = model.start_chat(history=[])

    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, 
        action="typing"
    )

    response = histori[user_id].send_message(pesan_user)
    jawaban = response.text

    await update.message.reply_text(jawaban)

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("clear", clear))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, balas))
    print("Bot berjalan...")
    app.run_polling()

if __name__ == "__main__":
    main()
