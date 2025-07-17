import asyncio
import logging
from pyrogram import Client
from pyrogram.errors import FloodWait, AuthKeyUnregistered, AuthKeyInvalid
import info
import os

# Enable logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize the client with better configuration
app = Client(
    "bot",
    api_id=info.API_ID,
    api_hash=info.API_HASH,
    bot_token=info.API_TOKEN,
    plugins=dict(root="plugins"),
    workdir="./",
    sleep_threshold=60,  # Sleep threshold for flood wait
    max_concurrent_transmissions=1  # Limit concurrent transmissions
)

async def start_bot_with_retry(max_retries=3):
    """Start the bot with retry logic and proper error handling"""
    for attempt in range(max_retries):
        try:
            logger.info(f"Starting bot (attempt {attempt + 1}/{max_retries})...")
            
            # Start the client
            await app.start()
            logger.info("✅ Bot started successfully!")
            
            # Get bot info
            me = await app.get_me()
            logger.info(f"Bot info: @{me.username} ({me.first_name})")
            
            # Keep the bot running
            await app.idle()
            break
            
        except FloodWait as e:
            logger.warning(f"⚠️ FloodWait error: Need to wait {e.x} seconds")
            
            if attempt == max_retries - 1:
                logger.error("❌ Max retries reached. Exiting...")
                return
                
            logger.info(f"⏳ Sleeping for {e.x} seconds...")
            await asyncio.sleep(e.x)
            
        except (AuthKeyUnregistered, AuthKeyInvalid) as e:
            logger.error(f"❌ Authentication error: {e}")
            logger.error("Please check your API_TOKEN, API_ID, and API_HASH")
            return
            
        except Exception as e:
            logger.error(f"❌ Unexpected error: {e}")
            
            if attempt == max_retries - 1:
                logger.error("❌ Max retries reached. Exiting...")
                return
                
            logger.info(f"⏳ Retrying in 30 seconds...")
            await asyncio.sleep(30)
    
    try:
        await app.stop()
        logger.info("Bot stopped gracefully")
    except:
        pass

if __name__ == "__main__":
    try:
        # Clear any existing session files to avoid conflicts
        session_files = ["bot.session", "bot.session-journal"]
        for file in session_files:
            if os.path.exists(file):
                os.remove(file)
                logger.info(f"Removed old session file: {file}")
        
        asyncio.run(start_bot_with_retry())
        
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
#     =API_TOKEN,
#     plugins={"root": "plugins"}
# )

# if __name__ == "__main__":
#     print(f"Starting {BOT_NAME}...")
#     app.run()
    
