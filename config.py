# Credit: @Hanimes_Hindi

import re
import os
from os import environ
from Script import script

id_pattern = re.compile(r'^.\d+$')
def is_enabled(value, default):
    if value.lower() in ["true", "yes", "1", "enable", "y"]:
        return True
    elif value.lower() in ["false", "no", "0", "disable", "n"]:
        return False
    else:
        return default
      
# Bot Information
API_ID = int(environ.get("API_ID", "6643753"))
API_HASH = environ.get("API_HASH", "88dfedc7b743512395bbd5153b201102")
BOT_TOKEN = environ.get("BOT_TOKEN", "5717147729:AAHf-p-YAP5Oyor4xKToTZKlr9TC6Wt1JOY")

PICS = (environ.get('PICS', 'https://i.ibb.co/KpzgscTP/7700112188-a0d84bee.jpg')).split() # Bot Start Picture
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ.get('ADMINS', '1327021082').split()]
BOT_USERNAME = environ.get("BOT_USERNAME", "RG_Files_Bot") # without @
PORT = environ.get("PORT", "8080")

# Clone Info :-
CLONE_MODE = bool(environ.get('CLONE_MODE', False)) # Set True or False

# If Clone Mode Is True Then Fill All Required Variable, If False Then Don't Fill.
CLONE_DB_URI = environ.get("CLONE_DB_URI", "")
CDB_NAME = environ.get("CDB_NAME", "clonetechvj")

# Database Information
DB_URI = environ.get("DB_URI", "mongodb+srv://poulomig644_db_user:d9MMUd5PsTP5MDFf@cluster0.q5evcku.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
DB_NAME = environ.get("DB_NAME", "techvjbotz")

# Auto Delete Information
AUTO_DELETE_MODE = bool(environ.get('AUTO_DELETE_MODE', True)) # Set True or False

# If Auto Delete Mode Is True Then Fill All Required Variable, If False Then Don't Fill.
AUTO_DELETE = int(environ.get("AUTO_DELETE", "30")) # Time in Minutes
AUTO_DELETE_TIME = int(environ.get("AUTO_DELETE_TIME", "1800")) # Time in Seconds

# Channel Information
LOG_CHANNEL = int(environ.get("LOG_CHANNEL", "-1001918476761"))

# File Caption Information
CUSTOM_FILE_CAPTION = environ.get("CUSTOM_FILE_CAPTION", f"{script.CAPTION}")
BATCH_FILE_CAPTION = environ.get("BATCH_FILE_CAPTION", CUSTOM_FILE_CAPTION)

# Enable - True or Disable - False
PUBLIC_FILE_STORE = is_enabled((environ.get('PUBLIC_FILE_STORE', "False")), True)

# Verification System 1
VERIFY_MODE_1 = bool(environ.get('VERIFY_MODE_1', True)) # Set True or False
SHORTLINK_URL_1 = environ.get("SHORTLINK_URL_1", "arolinks.com") # shortlink domain without https://
SHORTLINK_API_1 = environ.get("SHORTLINK_API_1", "2b3dd0b54ab06c6c8e6cf617f20d5fff15ee1b71") # shortlink api
VERIFY_TIME_1 = int(environ.get("VERIFY_TIME_1", "60")) # Verification time in seconds

# Verification System 2
VERIFY_MODE_2 = bool(environ.get('VERIFY_MODE_2', True)) # Set True or False
SHORTLINK_URL_2 = environ.get("SHORTLINK_URL_2", "arolinks.com") # shortlink domain without https://
SHORTLINK_API_2 = environ.get("SHORTLINK_API_2", "2b3dd0b54ab06c6c8e6cf617f20d5fff15ee1b71") # shortlink api
VERIFY_TIME_2 = int(environ.get("VERIFY_TIME_2", "60")) # Verification time in seconds

# Access time after first verification (default 30 minutes = 1800 seconds)
PASTIME = int(environ.get("PASTIME", "1800")) # Time in seconds

# Verification image URL (can be customized per user)
VERIFY_IMG = environ.get("VERIFY_IMG", "https://i.ibb.co/KpzgscTP/7700112188-a0d84bee.jpg")

# Website Info:
WEBSITE_URL_MODE = bool(environ.get('WEBSITE_URL_MODE', False)) # Set True or False

# If Website Url Mode Is True Then Fill All Required Variable, If False Then Don't Fill.
WEBSITE_URL = environ.get("WEBSITE_URL", "https://piracy-report.blogspot.com/2025/11/online.html") # For More Information Check Video On Yt - @Tech_VJ

# File Stream Config
STREAM_MODE = bool(environ.get('STREAM_MODE', False)) # Set True or False

# If Stream Mode Is True Then Fill All Required Variable, If False Then Don't Fill.
MULTI_CLIENT = False
SLEEP_THRESHOLD = int(environ.get('SLEEP_THRESHOLD', '60'))
PING_INTERVAL = int(environ.get("PING_INTERVAL", "1200"))  # 20 minutes
if 'DYNO' in environ:
    ON_HEROKU = True
else:
    ON_HEROKU = False
URL = environ.get("URL", "https://testofvjfilter-1fa60b1b8498.herokuapp.com/")
