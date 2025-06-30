import os
from utils.logger import logger
from telegram import Update

class FileUtils:

    def __init__(self):
        pass

    async def delete_file(self, path_to_file):
        try:
            os.remove(path_to_file)
            return True
        except Exception as err:
            print(err)

        return False


    async def send_file(self, bot, file_path: str, update: Update) -> None | bool:
        chat_id = update.effective_chat.id
        with open(file_path+'.enc', 'rb') as document:
            await bot.send_document(chat_id, document=document)
            logger.info(f"File {file_path} has sent to chat id -> {chat_id}")

        await self.delete_file(path_to_file=file_path)
        logger.info(f"File {file_path} has been deleted successfully.")
        await self.delete_file(path_to_file=file_path + '.enc')
        logger.info(f"File {file_path} has been deleted successfully.")