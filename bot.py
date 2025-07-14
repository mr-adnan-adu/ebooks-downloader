from pyrogram import Client
from info import API_ID, API_HASH, API_TOKEN, BOT_NAME

app = Client(
    name="eBookFilterBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=API_TOKEN,
    plugins={"root": "plugins"}
)

if __name__ == "__main__":
    print(f"Starting {BOT_NAME}...")
    app.run()
