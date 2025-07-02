import dotenv
from telegram.ext import Application, CommandHandler, ContextTypes, PrefixHandler
from telegram import Update


TOKEN = dotenv.get_key(key_to_get='TOKEN', dotenv_path='.env', encoding='utf-8')


if __name__ == '__main__':

    application = Application.builder().token(TOKEN).build()

    application.run_polling()
