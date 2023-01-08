import datetime
import logging

from telegram import Update
from telegram.constants import ParseMode
from telegram.error import BadRequest
from telegram.ext import ContextTypes

from teletwitterbot.database import List, session
from teletwitterbot.twitter_scraper import scrape_list

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Welcome to TeleTwitter Bot!")


async def showrecent(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot_list = session.query(List).filter_by(
        name=context.args[0], username=update.effective_user.username).one()
    tweets = scrape_list(bot_list)
    if len(tweets) == 0:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="No new tweets!")
    for tweet in tweets:
        try:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=tweet,
                                           parse_mode=ParseMode.MARKDOWN_V2)
        except BadRequest:
            logger.exception("Exception on sending message %s", tweet)

    bot_list.last_check = datetime.datetime.now() + datetime.timedelta(days=1)
