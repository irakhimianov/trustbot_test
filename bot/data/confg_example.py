import os

from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
ADMIN = os.getenv('ADMIN_ID')
ADMINS = [ADMIN, ]

SUGGESTION_CHAT = os.getenv('SUGGESTION_CHAT')
REQUEST_CHAT = os.getenv('REQUEST_CHAT')

PG_USER = os.getenv('PG_USER')
PG_PASSWORD = os.getenv('PG_PASSWORD')
PG_DATABASE = os.getenv('PG_DB')
PG_HOST = os.getenv('PG_HOST')
PG_PORT = os.getenv('PG_PORT')

REDIS_HOST = os.getenv('REDIS_HOST')
