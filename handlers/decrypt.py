from telegram import Update
from telegram.ext import ContextTypes, Application

class DecryptHandler:

    _application: Application

    def __init__(self):
        pass

    async def start(self, update: Update, context_type: ContextTypes.DEFAULT_TYPE):
        pass