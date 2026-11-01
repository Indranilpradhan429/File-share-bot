import re
import os
from os import environ
from Script import script

id_pattern = re.compile(r'^-?\d+$')

def is_enabled(value, default):
    if not value: 
        return default
    value = value.lower()
    if value in ["true", "yes", "1", "enable", "y"]:
        return True
    elif value in ["false", "no", "0", "disable", "n"]:
        return False
    else:
        return default
      
# Bot Information
API_ID = int(environ.get("API_ID", "31840117"))
API_HASH = environ.get("API_HASH", "89f1686ada0890abcfa567b211b70d1d")
BOT_TOKEN = environ.get("BOT_TOKEN", "9287123932:AAFa0Pch_5cmntLp8EP-pFdNSpeIPM43arI")

PICS = (environ.get('PICS', 'https://graph.org/file/ce1723991756e48c35aa1.jpg')).split()
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ.get('ADMINS', '').split() if admin]
BOT_USERNAME = environ.get("BOT_USERNAME", "Movietime17_bot")

# FIXED: PORT must be int for Render
PORT = int(environ.get("PORT", "8080"))

# Clone Info :-
CLONE_MODE = is_enabled(environ.get('CLONE_MODE', "False"), False)
CLONE_DB_URI = environ.get("CLONE_DB_URI", "mongodb+srv://Indranilp:indranil@cluster0.cbftbsc.mongodb.net/")
CDB_NAME = environ.get("CDB_NAME", "clonetechvj")

# Database Information
DB_URI = environ.get("DB_URI", "mongodb+srv://Indranilp:indranil@cluster0.cbftbsc.mongodb.net/")
DB_NAME = environ.get("DB_NAME", "techvjbotz")

# Auto Delete Information
AUTO_DELETE_MODE = is_enabled(environ.get('AUTO_DELETE_MODE', "True"), True)
AUTO_DELETE = int(environ.get("AUTO_DELETE", "5"))
AUTO_DELETE_TIME = int(environ.get("AUTO_DELETE_TIME", "300"))

# Channel Information - FIXED -100
LOG_CHANNEL = int(environ.get("LOG_CHANNEL", "-1003240202146"))

# File Caption Information
CUSTOM_FILE_CAPTION = environ.get("CUSTOM_FILE_CAPTION", f"{script.CAPTION}")
BATCH_FILE_CAPTION = environ.get("BATCH_FILE_CAPTION", CUSTOM_FILE_CAPTION)

PUBLIC_FILE_STORE = is_enabled(environ.get('PUBLIC_FILE_STORE', "False"), False)

# Verify Info :-
VERIFY_MODE = is_enabled(environ.get('VERIFY_MODE', "False"), False) # Default False korlam, jate verify jhamela na kore
SHORTLINK_URL = environ.get("SHORTLINK_URL", "arolinks.com")
SHORTLINK_API = environ.get("SHORTLINK_API", "25a1724f14b2699312d596a7d2e7a9adf8cf865f")
VERIFY_TUTORIAL = environ.get("VERIFY_TUTORIAL", "https://t.me/backup_movietime/6")

WEBSITE_URL_MODE = is_enabled(environ.get('WEBSITE_URL_MODE', "False"), False)
WEBSITE_URL = environ.get("WEBSITE_URL", "")

STREAM_MODE = is_enabled(environ.get('STREAM_MODE', "False"), False)
MULTI_CLIENT = False
SLEEP_THRESHOLD = int(environ.get('SLEEP_THRESHOLD', '60'))
PING_INTERVAL = int(environ.get("PING_INTERVAL", "1200"))
ON_HEROKU = 'DYNO' in environ
URL = environ.get("URL", "")
