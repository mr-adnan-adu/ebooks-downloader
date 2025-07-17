from pyrogram import Client, filters
from database import ebooks_collection
from utils import format_result

# Custom filter to exclude commands
def not_command_filter(_, __, message):
    return not message.text.startswith("/")

search_filter = filters.group & filters.text & filters.create(not_command_filter)

@Client.on_message(search_filter)
async def auto_filter(client, message):
    query = message.text
    results = ebooks_collection.find({
        "$or": [
            {"title": {"$regex": query, "$options": "i"}},
            {"author": {"$regex": query, "$options": "i"}},
            {"genre": {"$regex": query, "$options": "i"}}
        ]
    }).limit(5)
    for result in results:
        await message.reply_text(format_result(result))
