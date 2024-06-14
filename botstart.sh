#!/bin/bash

cd ~/speedtest_bot
source .venv/bin/activate
python3 main.py >> bot.log 2>> bot.errors
