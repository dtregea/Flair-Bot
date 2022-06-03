"""
Flair-Bot
Automatically assign flairs from your subreddit to posters without one
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


# Stream of newest posts and comments
def submissions_and_comments(subreddit: SUBREDDIT_TYPE, **kwargs):
    new_posts = []
    new_posts.extend(subreddit.new(**kwargs))
    new_posts.extend(subreddit.comments(**kwargs))
    new_posts.sort(key=lambda post: post.created_utc, reverse=True)
    return new_posts


# Get flairs from a subreddit
def get_flairs(subreddit: SUBREDDIT_TYPE):
    flairs = []
    for flair in subreddit.flair.templates.__iter__():
        flairs.append(flair)
    return flairs


while True:
    stream = praw.reddit.models.subreddits.stream_generator(
        lambda **kwargs: submissions_and_comments(TARGET_SUBREDDIT, **kwargs), skip_existing=True)
    try:
        print("Listening...")
        while True:
            for post in stream:
                print(
                    ('Comment' if isinstance(post, COMMENT_TYPE) else 'Submission') + " by \'" + str(
                        post.author) + "\' - \'" + (str(post.body) if isinstance(post, COMMENT_TYPE) else str(post.title)) + "\'")
                try:
                    if post.author not in config.IGNORED_USERS:
                        # Delete cross-posts from r/repost
                        if hasattr(post, "crosspost_parent"):
                            original_sub_name = reddit.submission(id=post.crosspost_parent.split("_")[1]).subreddit
                            if original_sub_name == 'repost':
                                print("Removing spam post")
                                post.mod.remove()
                                post.mod.send_removal_message(message=config.REMOVAL_MESSAGE,
                                                              type='public')
                        # Assign random flairs to posters without one
                        if post.author_flair_text is None:
                            randFlair = random.choice(get_flairs(TARGET_SUBREDDIT))
                            print("Setting flair for " + str(post.author) + ": ", randFlair['text'])
                            TARGET_SUBREDDIT.flair.set(post.author, text=randFlair['text'],
                                                       css_class=randFlair['css_class'],
                                                       flair_template_id=randFlair['id'])
                except Exception as e:
                    print(e, file=sys.stderr)
    except Exception as e:
        print(e, file=sys.stderr)
        print("Attempting to reconnect...")
