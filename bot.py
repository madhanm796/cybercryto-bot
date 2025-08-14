import threading

import dotenv
import os

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
    ContextTypes
)

from enums.Enum import UPLOAD_FOLDER

from handlers.start import StartHandler
from handlers.encrypt import EncryptHandler
from handlers.decrypt import DecryptHandler

from flask import Flask

TOKEN = dotenv.get_key(key_to_get='TOKEN', dotenv_path='.env', encoding='utf-8')

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is alive!", 200


def run_web():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

def main():

    application = Application.builder().token(TOKEN).build()

    start_handler = StartHandler()
    encrypt_handler = EncryptHandler()
    decrypt_handler = DecryptHandler()

    encrypt_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("encrypt", encrypt_handler.start)],
        states={
            encrypt_handler.ASK_FILE:[MessageHandler(filters.Document.ALL, encrypt_handler.ask_file)],
            encrypt_handler.ASK_ENCRYPTION_METHOD:[MessageHandler(filters.TEXT & (~filters.COMMAND), encrypt_handler.ask_method)]
        },
        fallbacks=[
            CommandHandler("cancel", encrypt_handler.cancel)
        ]
    )

    decrypt_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("decrypt", decrypt_handler.start)],
        states={
            decrypt_handler.ASK_FILE:[MessageHandler(filters.Document.ALL, decrypt_handler.ask_file)],
            decrypt_handler.ASK_KEY_FILE:[MessageHandler(filters.Document.ALL, decrypt_handler.ask_key_file)],
            decrypt_handler.ASK_DECRYPTION_METHOD:[MessageHandler(filters.TEXT & (~filters.COMMAND), decrypt_handler.ask_method)]
        },
        fallbacks=[
            CommandHandler("cancel", decrypt_handler.cancel)
        ]
    )

    application.add_handler(CommandHandler("start", start_handler.start))
    application.add_handler(CommandHandler("help", start_handler.help))

    application.add_handlers(
        [
            encrypt_conv_handler,
            decrypt_conv_handler
        ]
    )

    # application.add_error_handler(error)

    application.run_polling()


if __name__ == '__main__':

    os.makedirs(os.path.join(os.curdir, UPLOAD_FOLDER), exist_ok=True)
    threading.Thread(target=run_web, daemon=True).start()

    import asyncio

    asyncio.run(main())
