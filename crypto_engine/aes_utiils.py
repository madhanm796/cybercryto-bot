import tempfile

from telegram import Update

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

import os

from telegram.ext import Application

from utils.file_utils import FileUtils


class AESUtil:

    _update: Update
    _upload_folder: str = os.path.join(os.curdir + 'uploads')
    _application: Application

    def __init__(self, update: Update, application: Application):
        self._update = update
        self._application = application

    async def encrypt(self, file_path: any, file_name: str) -> bool | None:

        key:bytes = get_random_bytes(16)
        iv: bytes = get_random_bytes(16)

        plain_text:bytes

        try:
            with open(file_path, 'rb') as file:
                plain_text = file.read()

            cipher = AES.new(key, AES.MODE_GCM, iv)
            cipher_text = cipher.encrypt(pad(plain_text, AES.block_size))

            with open(file_path +'.enc', 'wb') as file:
                file.write(iv+cipher_text)

            await self._update.message.reply_text(f"File successfully encrypted!\nkey => <b>{key.hex()}</b>", parse_mode='HTML')

            return True

        except Exception as e:
            print(e)

        return False