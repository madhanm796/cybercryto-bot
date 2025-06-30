from os.path import exists

from telegram import Update
from telegram.ext import ContextTypes, PrefixHandler, Application, MessageHandler, filters
from telegram import InputFile
import os
from utils.file_utils import FileUtils
from crypto_engine.aes_utiils import AESUtil

from utils.logger import logger

UPLOAD_DIR = "uploads"

class EncryptHandler:

    _application: Application
    _file_handler = FileUtils()

    def __init__(self, application):
        self._application = application
        os.makedirs(os.path.join(os.curdir, UPLOAD_DIR), exist_ok=True)

    async def handle_aes_encrypt(self, update: Update, context_type: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Please upload a file to encrypted (in a document format, not a photo or compressed data)")

        self._application.add_handler(MessageHandler(filters.Document.ALL, self.handle_file))

    async def handle_file(self, update: Update, context_type: ContextTypes.DEFAULT_TYPE):

        aes = AESUtil(update, self._application)
        document = update.message.document

        file = await context_type.bot.get_file(document.file_id)
        file_path = os.path.join(UPLOAD_DIR, document.file_unique_id)

        await file.download_to_drive(file_path)

        await update.message.reply_text(f"File {document.file_name} was uploaded successfully")
        await update.message.reply_text("Please wait... your file is being encrypted.")

        if await aes.encrypt(file_path, document.file_name):
            await self._file_handler.send_file(
                bot=self._application.bot,
                file_path=file_path,
                update=update)
