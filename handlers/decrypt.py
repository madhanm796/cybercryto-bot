from telegram import Update
from telegram.ext import ContextTypes, Application, ConversationHandler, MessageHandler, filters

from helpers.helpers import Helpers
from utils.AESUtils import AESUtils

class DecryptHandler:

    _application: Application
    _helpers: Helpers
    ASK_FILE, ASK_KEY_FILE, ASK_DECRYPTION_METHOD = range(3)

    def __init__(self):
        pass

    async def start(self, update: Update, context_type: ContextTypes.DEFAULT_TYPE):

        await update.message.reply_text("Please upload the file which you want to be decrypted.")
        return self.ASK_FILE

    async def ask_file(self, update: Update, context_type: ContextTypes.DEFAULT_TYPE):

        self._helpers = Helpers(update, context_type)

        file = await self._helpers.save_file()
        self.file = file[-1]    

        await update.message.reply_text("Please upload the key file to perform decryption.")
        return self.ASK_KEY_FILE
    
    async def ask_key_file(self, update: Update, context_type: ContextTypes.DEFAULT_TYPE):
        self._helpers = Helpers(update, context_type)

        file = await self._helpers.save_file(ext='.key')
        self.key = file[-1]

        await update.message.reply_text("Please choose the decryption method...\n1. AES\n\nExample: AES\n\nMore options will added in the future.")
        return self.ASK_DECRYPTION_METHOD

    async def ask_method(self, update: Update, context_type: ContextTypes.DEFAULT_TYPE):

        method = update.message.text.lower().strip()

        if method == 'aes':
            aes = AESUtils(update, context_type)
            if not await aes.decrypt(self.file, self.key):
                await update.message.reply_text("Operation failed...")
                return
            await update.message.reply_text("Decryption successful")  

        else:
            await update.message.reply_text("Operation not permitted, Reason: invalid decryption method chosen.")

        return ConversationHandler.END
