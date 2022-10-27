import datetime
import logging

from telegram import Update
from telegram.constants import ParseMode
from telegram.error import BadRequest
from telegram.ext import ContextTypes

from teletwitterbot.database import List, Member, session
from teletwitterbot.twitter_scraper import scrape_list

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Welcome to TeleTwitter Bot!")


async def createlist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot_list = List(name=context.args[0],
                    username=update.effective_user.username,
                    last_check=datetime.datetime.now() -
                    datetime.timedelta(days=2))
    session.add(bot_list)
    session.commit()
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"List {bot_list.name} Added Successfully")


async def addtolist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    member_username = context.args[0]
    bot_list = session.query(List).filter_by(
        name=context.args[1], username=update.effective_user.username).one()
    member = Member(list=bot_list, username=member_username)
    session.add(member)
    session.commit()
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Member {member.username} added to list {member.list.name}")


async def showrecent(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot_list = session.query(List).filter_by(
        name=context.args[0], username=update.effective_user.username).one()
    tweets = scrape_list(bot_list)
    for tweet in tweets:
        try:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=tweet,
                                           parse_mode=ParseMode.MARKDOWN_V2)
        except BadRequest:
            logger.exception("Exception on sending message %s", tweet)

    bot_list.last_check = datetime.datetime.now()
