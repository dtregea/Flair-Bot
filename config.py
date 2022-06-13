import os

CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
BOT_USERNAME = os.environ.get('BOT_USERNAME')  # Bot Account Username
BOT_PASSWORD = os.environ.get('BOT_PASSWORD')  # Bot Account Password
USER_AGENT = os.environ.get('USER_AGENT')  # Program Identifier for Reddit
TARGET_SUB = os.environ.get('TARGET_SUB')  # Subreddit to moderate
REMOVAL_MESSAGE = os.environ.get('REMOVAL_MESSAGE') # Removal message for spam posts
AUTO_MAIL_REPLY = os.environ.get('AUTO_MAIL_REPLY') #
AUTO_MAIL_ON = os.environ.get('AUTO_MAIL_ON') # True or False
IGNORED_USERS = ["AutoModerator", BOT_USERNAME]  # Users to not respond to