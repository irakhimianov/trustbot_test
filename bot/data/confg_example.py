import os

from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
ADMIN = os.getenv('ADMIN_ID')
ADMINS = [ADMIN, ]
SUGGESTION_CHAT = os.getenv('SUGGESTION_CHAT')
REQUEST_CHAT = os.getenv('REQUEST_CHAT')
