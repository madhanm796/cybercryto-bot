from telegram import Update
from telegram.ext import ContextTypes

async def error(update: Update, context_type:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Invalid command. Please provide a valid one.')