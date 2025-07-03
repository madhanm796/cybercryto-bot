import os

from telegram import Update
from telegram.ext import ContextTypes

from enums.Enum import UPLOAD_FOLDER

class Helpers:

    _update: Update
    _context_type: ContextTypes.DEFAULT_TYPE

    def __init__(self, update:Update, context_type: ContextTypes.DEFAULT_TYPE):
        self._update = update
        self._context_type = context_type

    async def save_file(self):
        # Getting the file
        document = self._update.message.document

        file = await self._context_type.bot.get_file(document.file_id)
        # Defining path to save the file

        file_path = os.path.join(UPLOAD_FOLDER, document.file_unique_id)
        
        # Saving the file to local drive
        await  file.download_to_drive(file_path)

        return (document, file_path)

    async def read_file(self, path: str) -> bytes | None:

        data: bytes

        with open(path, 'rb') as file:
            data = file.read()

        return data
    
    async def write_file(self, path: str, data: bytes) -> bool | None:
        
        with open(path, 'wb') as file:
            file.write(data)

        return os.path.exists(path)
    
    async def send_file(self, file_path: str) -> bool | None:
        chat_id = self._update.effective_chat.id
        flag: bool = False

        try:
            with open(file_path, 'rb') as document:
                await self._context_type.bot.send_document(chat_id=chat_id, 
                                                           document=document.read(),
                                                           filename=document.name)

            flag = True

        except Exception as e:
            print(e)

        return flag