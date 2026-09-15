#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration file for US Student Email Telegram Bot
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Configuration
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
TELEGRAM_ADMIN_ID = int(os.getenv('TELEGRAM_ADMIN_ID', '0'))

# Database Configuration
DB_HOST = os.getenv('DB_HOST', '127.0.0.1')
DB_PORT = int(os.getenv('DB_PORT', '3306'))
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_NAME = os.getenv('DB_NAME', 'student_email')

# Application Configuration
BROWSER_TIMEOUT = 60000  # milliseconds
DEFAULT_PASSWORD = os.getenv('DEFAULT_PASSWORD', 'qaz2020')
DEFAULT_PIN = os.getenv('DEFAULT_PIN', '9210')
WAIT_TIME = 1000  # milliseconds

# Logging Configuration
LOG_FILE = 'bot.log'
LOG_LEVEL = 'INFO'

# Browser Configuration
BROWSER_HEADLESS = True
BROWSER_WIDTH = 1920
BROWSER_HEIGHT = 1080
