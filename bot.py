import asyncio
import logging
import signal
import sys
from pyrogram import Client
from pyrogram.errors import FloodWait, AuthKeyUnregistered, AuthKeyInvalid
import info
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global variable to track if bot is running
bot_running = False

# Initialize the client
app = Client(
    "bot",
    api_id=info.API_ID,
    api_hash=info.API_HASH,
    bot_token=info.API_TOKEN,
    plugins=dict(root="plugins"),
    workdir="./",
    sleep_threshold=60,
    max_concurrent_transmissions=1
)

async def stop_bot():
    """Gracefully stop the bot"""
    global bot_running
    try:
        if bot_running and app.is_connected:  # Fixed: was "not app.is_connected"
            await app.stop()
            logger.info("✅ Bot stopped gracefully")
    except Exception as e:
        logger.error(f"Error stopping bot: {e}")
    finally:
        bot_running = False

def signal_handler(sig, frame):
    """Handle shutdown signals"""
    logger.info("Received shutdown signal")
    loop = asyncio.get_event_loop()
    if loop.is_running():
        loop.create_task(stop_bot())
    sys.exit(0)

async def start_bot():
    """Start the bot with proper error handling"""
    global bot_running
    
    try:
        # Check if already connected
        if app.is_connected:
            logger.warning("Client is already connected")
            return
        
        logger.info("Starting bot...")
        
        # Start the client
        await app.start()
        bot_running = True
        
        # Get bot info
        try:
            me = await app.get_me()
            logger.info(f"✅ Bot started successfully!")
            logger.info(f"Bot info: @{me.username} ({me.first_name})")
        except Exception as e:
            logger.error(f"Could not get bot info: {e}")
        
        # Keep the bot running
        logger.info("Bot is running... Press Ctrl+C to stop")
        await app.idle()
        
    except FloodWait as e:
        # Fixed: Use e.value instead of e.x for newer Pyrogram versions
        wait_time = getattr(e, 'value', getattr(e, 'x', 30))
        logger.warning(f"⚠️ FloodWait error: Need to wait {wait_time} seconds")
        logger.info(f"⏳ Waiting for {wait_time} seconds...")
        await asyncio.sleep(wait_time)
        logger.info("Retrying after FloodWait...")
        await start_bot()
        
    except (AuthKeyUnregistered, AuthKeyInvalid) as e:
        logger.error(f"❌ Authentication error: {e}")
        logger.error("Please check your API_TOKEN, API_ID, and API_HASH in info.py")
        return
        
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        logger.error("This might be a plugin error. Check your plugins folder.")
        return
    
    finally:
        await stop_bot()

def main():
    """Main function to run the bot"""
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # Clear any existing session files to avoid conflicts
        session_files = ["bot.session", "bot.session-journal"]
        for file in session_files:
            if os.path.exists(file):
                os.remove(file)
                logger.info(f"Removed old session file: {file}")
        
        # Run the bot
        asyncio.run(start_bot())
        
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
    
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
    
