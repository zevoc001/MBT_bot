import os

from dotenv import load_dotenv

load_dotenv('../config.env')

TOKEN = os.getenv('TOKEN')
DB_URL = os.getenv('DB_URL')
DB_ACCESS_TOKEN = os.getenv('DB_ACCESS_TOKEN')
HELP_BOT_LINK = os.getenv('HELP_BOT_LINK')
