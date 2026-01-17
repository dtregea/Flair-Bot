"""
Flair-Bot
Automatically assign flairs from your subreddit to posters without one,
remove cross-posts from unwanted subreddits, and auto-respond to mod-mail
"""

import sys
import praw
import random
import config

reddit = praw.Reddit(client_id=config.CLIENT_ID,
                     client_secret=config.CLIENT_SECRET,
                     username=config.BOT_USERNAME,
                     password=config.BOT_PASSWORD,
                     user_agent=config.USER_AGENT)
TARGET_SUBREDDIT = reddit.subreddit(config.TARGET_SUB)

# Useful Type Constants
SUBMISSION_TYPE = praw.reddit.models.Submission
COMMENT_TYPE = praw.reddit.models.Comment
SUBREDDIT_TYPE = praw.reddit.models.Subreddit
MODMAIL_TYPE = praw.reddit.models.ModmailConversation


# Stream of newest posts, comments, and mod-mail conversations
def get_submissions_comments_modmail(subreddit: SUBREDDIT_TYPE, **kwargs):
    new_posts = []
    new_posts.extend(subreddit.modmail.conversations(state="all"))
    new_posts.extend(subreddit.new(**kwargs))
    new_posts.extend(subreddit.comments(**kwargs))
    return new_posts


# Get flairs from a subreddit
def get_flairs(subreddit: SUBREDDIT_TYPE):
    flairs = []
    for flair in subreddit.flair.templates.__iter__():
        flairs.append(flair)
    return flairs


while True:
    try:
        stream = praw.reddit.models.subreddits.stream_generator(
            lambda **kwargs: get_submissions_comments_modmail(TARGET_SUBREDDIT, **kwargs), skip_existing=True,
            attribute_name='id')
        print("Listening on subreddit: " + config.TARGET_SUB)
        while True:
            for stream_item in stream:
                try:
                    if stream_item is None:
                        continue
                    if hasattr(stream_item, "author") and stream_item.author in config.IGNORED_USERS:
                        continue

                    # Mod mail
                    if config.AUTO_MAIL_ON and isinstance(stream_item, MODMAIL_TYPE):
                        print("Responding to new mod mail")
                        mail: MODMAIL_TYPE = stream_item
                        mail.reply(config.AUTO_MAIL_REPLY)

                    # Posts
                    if isinstance(stream_item, SUBMISSION_TYPE):
                        # Delete cross-posts from r/repost
                        print(
                            ("Submission by \'" + str(
                                stream_item.author) + "\' - \'" + str(stream_item.title)) + "\'")
                        if hasattr(stream_item, "crosspost_parent"):
                            original_sub_name = reddit.submission(id=stream_item.crosspost_parent.split("_")[1]).subreddit
                            if original_sub_name == 'repost':
                                print("Removing spam post")
                                stream_item.mod.remove()
                                stream_item.mod.send_removal_message(message=config.REMOVAL_MESSAGE,
                                                                     type='public')
                    # Comments
                    if isinstance(stream_item, COMMENT_TYPE):
                        print(
                            "Comment by \'" + str(
                                stream_item.author) + "\' - \'" + str(stream_item.body) + "\'")

                    # Comments or posts
                    if isinstance(stream_item, COMMENT_TYPE) or isinstance(stream_item, SUBMISSION_TYPE):
                        if stream_item.author_flair_text is None:
                            randFlair = random.choice(get_flairs(TARGET_SUBREDDIT))
                            print("Setting flair for " + str(stream_item.author) + ": ", randFlair['text'])
                            TARGET_SUBREDDIT.flair.set(stream_item.author, text=randFlair['text'],
                                                       css_class=randFlair['css_class'],
                                                       flair_template_id=randFlair['id'])
                except Exception as e:
                    print(e, file=sys.stderr)

    except Exception as e:
        print(e, file=sys.stderr)
        print("Attempting to reconnect...")
