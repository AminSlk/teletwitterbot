import datetime
import logging

from Scweet.scweet import scrape

from teletwitterbot.config import settings
from teletwitterbot.database import List

logger = logging.getLogger(__name__)


def scrape_list(bot_list: List):
    tweets_df = None
    for member in bot_list.members:
        member_tweets = get_user_tweets(member.username, bot_list.last_check)
        if tweets_df is None:
            tweets_df = member_tweets
        else:
            tweets_df = tweets_df.append(member_tweets, ignore_index=True)
    tweets = tweets_df.sort_values('Timestamp')
    return create_message_from_tweets(tweets)


def create_message_from_tweets(tweets):
    messages = []
    for _, tweet in tweets.iterrows():
        message = f"""From {tweet['UserName']}: \n\n
                    {tweet['Embedded_text']} \n\n
                    [Tweet Link]({tweet['Tweet URL']})"""
        message = message.replace('.', r'\.')
        message = message.replace('-', r'\-')
        message = message.replace('#', r'\#')
        messages.append(message)
    return messages


def get_user_tweets(username, from_date: datetime.datetime):
    tweets = scrape(since=from_date.strftime("%Y-%m-%d"),
                    interval=1,
                    from_account=username,
                    headless=True,
                    filter_replies=True,
                    proxy=settings["proxy_url"])
    return tweets
