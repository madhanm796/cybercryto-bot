from telegram import Update, ForceReply, InlineKeyboardMarkup
from telegram.ext import ContextTypes


class StartHandler:


    async def start(self, update: Update, context_types: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Hello, World")


    async def description(self, update: Update, context_type: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(StartHandler.get_description(), parse_mode='HTML')

    @classmethod
    def get_description(cls):
        return """
        <b>🤖 CyberCrypt Bot</b>

        <i>Secure. Simple. Smart.</i>
        
        CyberCrypt Bot is a secure, lightweight, and intelligent assistant designed to help users <b>encrypt, decrypt, and hash</b> their files or messages using cryptographic algorithms like <b>AES, RSA, and SHA-256</b>.
        
        Whether you're a cybersecurity student, ethical hacker, or privacy-focused user, CyberCrypt performs all operations <u>temporarily in memory</u> and does <b>not store any of your data</b>.
        
        <b>⚠️ Terms & Conditions</b>
        
        <pre>By using CyberCrypt Bot, you agree to the following:</pre>
        
        <b>1. Educational Use Only</b>
        <i>This bot is for personal and educational use only. Misuse for illegal activity is prohibited.</i>
        
        <b>2. No Data Storage</b>
        CyberCrypt does not store or log your files, messages, or encryption keys. All actions are processed in RAM and discarded afterward.
        
        <b>3. User Responsibility</b>
        Users are responsible for what they encrypt/decrypt using this bot. The developer holds no liability for data misuse.
        
        <b>4. Security Notice</b>
        Although strong cryptographic libraries are used, this bot is not a replacement for enterprise-grade systems. Use at your own risk.
        
        <b>5. Fair Usage</b>
        Misuse, automation, or abuse of the bot may lead to restrictions or permanent bans.

        <b>🔐 Supported Features</b>
        • AES 256-bit File Encryption/Decryption  
        • RSA Encryption (Public/Private Key)  
        • Hashing with SHA-256 & SHA-512  
        
        """
