from telegram import Update
from telegram.ext import ContextTypes

class StartHandler:

    def __init__(self):
        pass

    async def start(self, update: Update, context_type: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Welcome to "+update.get_bot().first_name)
        