import dotenv
from telegram.ext import Application, CommandHandler, ContextTypes, PrefixHandler
from telegram import Update

from utils.logger import logger

from handlers.encrypt_handler import EncryptHandler
from handlers.start_handler import StartHandler

TOKEN = dotenv.get_key(key_to_get='TOKEN', dotenv_path='.env', encoding='utf-8')


if __name__ == '__main__':

    application = Application.builder().token(TOKEN).build()
    logger.log(level=0, msg="Application started")

    start_handler = StartHandler()
    encrypt_handler = EncryptHandler(application)

    application.add_handler(CommandHandler("start", start_handler.start))
    application.add_handler(CommandHandler("description", start_handler.description))


    application.add_handler(PrefixHandler("?", "encrypt_aes", encrypt_handler.handle_aes_encrypt))


    application.run_polling()
