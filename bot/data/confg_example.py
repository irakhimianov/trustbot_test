import os

from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
ADMIN = os.getenv('ADMIN_ID')
ADMINS = []