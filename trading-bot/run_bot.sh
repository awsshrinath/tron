#!/bin/bash
cd /home/tts_api1/trading-bot
source venv/bin/activate
export ZERODHA_API_KEY="y1fdzvfvfh6rwqbb"
export ZERODHA_API_SECRET="rlx3rx7cls6g2iv1mddq89s593245jof"
export ZERODHA_ACCESS_TOKEN="2dQ5FS7mapQKTpOYhMpfFzDRhXy8ibcx"
python3 bot.py >> bot.log 2>&1
