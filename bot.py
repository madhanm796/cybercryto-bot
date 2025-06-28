import dotenv
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram import Update

from handlers.start_handler import StartHandler

TOKEN = dotenv.get_key(key_to_get='TOKEN', dotenv_path='.env', encoding='utf-8')

async def start(update: Update, contextType: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello, World")


if __name__ == '__main__':


    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", StartHandler.start))
    application.add_handler(CommandHandler("description", StartHandler.description))

    application.run_polling()
