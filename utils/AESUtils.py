from telegram import Update
from telegram.ext import ContextTypes

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

from helpers.helpers import Helpers

class AESUtils:

    _update: Update
    _context_type: ContextTypes.DEFAULT_TYPE
    _helper: Helpers

    def __init__(self, update: Update, context_type: ContextTypes.DEFAULT_TYPE):
        self._update = update
        self._context_type = context_type
        self._helper = Helpers(self._update, self._context_type)

    async def encrypt(self, file_path: str) -> bool | None:
        
        key: bytes = get_random_bytes(16)
        iv: bytes = get_random_bytes(16)


        try:
            data = await self._helper.read_file(file_path)

            cipher = AES.new(key, AES.MODE_GCM, iv)
            cipher_text = cipher.encrypt(pad(data, AES.block_size))

            file_path = file_path + '.enc'
            path_to_key: str = file_path.split('.')[0]+'.key'

            if not await self._helper.write_file(file_path, iv+cipher_text):
                await self._update.message.reply_text("Operation failed...")
                return
            
            if not await self._helper.send_file(file_path):
                await self._update.message.reply_text("Operation failed...")
                return
                        
            if not await self._helper.write_file(path_to_key, key.hex().encode('utf-8')):
                print("Unable to write key to a separate file.")
                return
            
            if not await self._helper.send_file(path_to_key):
                await self._update.message.reply_text("Operation failed...")
                return

            return True

        except Exception as err:
            print(err)

        return False


    async def decrypt(self, file_path: str, key_path: str) -> bool | None:
        
        try:
            key = await self.extract_key(key_path)

            raw = await self._helper.read_file(file_path)

            iv = raw[:16]
            cipher_text = raw[16:]
            decrypter = AES.new(key, AES.MODE_GCM, iv)
            unchiper_text = unpad(decrypter.decrypt(cipher_text), AES.block_size)

            decryption_path = file_path +'.dec'

            if not await self._helper.write_file(decryption_path, unchiper_text):
                return
    
            if not await self._helper.send_file(decryption_path):
                return

            return True
                        

        except Exception as err:
            print(err)

        return False

    async def extract_key(self, key: str) -> bytes | None:
        key: str

        try:
            with open(key, 'r') as f:
                key = f.read()
        except Exception as err:
            print(err)

        return bytes.fromhex(key)


        