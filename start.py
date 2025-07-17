from pyrogram import Client, filters
from pyrogram.types import Message

@Client.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
    """Handle /start command"""
    await message.reply_text(
        "🤖 **Bot is working!**\n\n"
        "Available commands:\n"
        "/start - Start the bot\n"
        "/ping - Check bot status\n\n"
        "Bot is running successfully!"
    )

@Client.on_message(filters.command("ping"))
async def ping_command(client: Client, message: Message):
    """Handle /ping command"""
    await message.reply_text("🏓 Pong! Bot is online.")
