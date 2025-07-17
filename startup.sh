#!/bin/bash

# Clear any existing session files
rm -f bot.session*

# Wait a bit to avoid immediate restart conflicts
sleep 10

# Start the bot
python3 bot.py
