import asyncio
import logging
from pyrogram import Client
from pyrogram.errors import FloodWait
import info

# Enable logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the client
app = Client(
    "bot",
    api_id=info.API_ID,
    api_hash=info.API_HASH,
    bot_token=info.API_TOKEN,
    plugins=dict(root="plugins")
)

async def start_bot():
    """Start the bot with proper error handling"""
    try:
        await app.start()
        logger.info("Bot started successfully!")
        
        # Keep the bot running
        await app.idle()
        
    except FloodWait as e:
        logger.warning(f"FloodWait error: Need to wait {e.x} seconds")
        logger.info(f"Sleeping for {e.x} seconds...")
        await asyncio.sleep(e.x)
        
        # Try to start again after waiting
        logger.info("Attempting to restart after FloodWait...")
        await start_bot()
        
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise e
    
    finally:
        await app.stop()

if __name__ == "__main__":
    try:
        asyncio.run(start_bot())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot failed to start: {e}")

# from pyrogram import Client
# from info import API_ID, API_HASH, API_TOKEN, BOT_NAME

# app = Client(
#     name="eBookFilterBot",
#     api_id=API_ID,
#     api_hash=API_HASH,
#     bot_token=API_TOKEN,
#     plugins={"root": "plugins"}
# )

# if __name__ == "__main__":
#     print(f"Starting {BOT_NAME}...")
#     app.run()
    
