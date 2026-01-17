import os

from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.environ.get('MOD_CLIENT_ID')
CLIENT_SECRET = os.environ.get('MOD_CLIENT_SECRET')
BOT_USERNAME = os.environ.get('MOD_BOT_USERNAME')  # Bot Account Username
BOT_PASSWORD = os.environ.get('MOD_BOT_PASSWORD')  # Bot Account Password
USER_AGENT = os.environ.get('MOD_USER_AGENT')  # Program Identifier for Reddit
TARGET_SUB = os.environ.get('MOD_TARGET_SUB')  # Subreddit to moderate
REMOVAL_MESSAGE = os.environ.get('MOD_REMOVAL_MESSAGE')  # Removal message for spam posts
AUTO_MAIL_REPLY = os.environ.get('MOD_AUTO_MAIL_REPLY')
AUTO_MAIL_ON = (os.environ.get('MOD_AUTO_MAIL_ON', '') or '').strip().lower() == 'true'
IGNORED_USERS = ["AutoModerator", BOT_USERNAME]  # Users to not respond to