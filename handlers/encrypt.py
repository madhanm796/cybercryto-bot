from telegram import Update, File
from telegram.ext import Application, ContextTypes, ConversationHandler
from enums.Enum import UPLOAD_FOLDER

from helpers.helpers import Helpers
from utils.AESUtils import AESUtils

class EncryptHandler:

    ASK_FILE, ASK_ENCRYPTION_METHOD = range(2)

    _application: Application

    def __init__(self):
        pass

    async def start(self, update: Update, context_type: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Please upload a file to encrypt...")
        return self.ASK_FILE

    async def ask_file(self, update: Update, context_type: ContextTypes.DEFAULT_TYPE):

        helper = Helpers(update, context_type)
        document, file_path = await helper.save_file()
        self._file_path = file_path

        file_name = document.file_name
        
        await update.message.reply_text(f"File {file_name} is uploaded successfully.")

        await update.message.reply_text("Choose encryption method... \n1. AES\n\nExample: AES\n\nMore options will added in the future.")


        return self.ASK_ENCRYPTION_METHOD
    
    async def ask_method(self, update: Update, context_type: ContextTypes.DEFAULT_TYPE):
        message = update.message.text.lower().strip()

        if message == 'aes':
            aes = AESUtils(update, context_type)
            if await aes.encrypt(self._file_path):
                await update.message.reply_text("Encryption successful")
            else:
                await update.message.reply_text("Encryption failed")
        elif message == 'rsa':
            print("Choosen RSA encryption")
        
        return ConversationHandler.END
    
