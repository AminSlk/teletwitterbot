import datetime
import logging

from Scweet.scweet import scrape

from teletwitterbot.config import Config
from teletwitterbot.database import List

logger = logging.getLogger(__name__)


def scrape_list(bot_list: List):
    tweets_df = None
    for member in bot_list.members:
        member_tweets = get_user_tweets(member.username, bot_list.last_check)
        if not tweets_df:
            tweets_df = member_tweets
        else:
            tweets_df = tweets_df.append(member_tweets, ignore_index=True)
    tweets_links = list(tweets_df.sort_values('Timestamp')['Tweet URL'])
    return tweets_links


def get_user_tweets(username, from_date: datetime.datetime):
    tweets = scrape(since=from_date.strftime("%Y-%m-%d"),
                    interval=1,
                    from_account=username,
                    headless=True,
                    filter_replies=True,
                    proxy=Config["proxy_url"])
    return tweets
