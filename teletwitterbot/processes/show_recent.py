import datetime
import logging

from telegram import Update
from telegram.constants import ParseMode
from telegram.error import BadRequest
from telegram.ext import (CommandHandler, ContextTypes, ConversationHandler,
                          MessageHandler, filters)

from teletwitterbot.database import List, session
from teletwitterbot.processes.commons import cancel
from teletwitterbot.twitter_scraper import scrape_list

logger = logging.getLogger(__name__)

GETLISTNAME = range(1)

async def showrecent(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Please send the list name!")
    return GETLISTNAME

async def get_list_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    list_name = update.message.text
    bot_list = session.query(List).filter_by(
        name=list_name, username=update.effective_user.username).one()
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
    return ConversationHandler.END


def get_handler():
    handler = ConversationHandler(
        entry_points=[CommandHandler('showrecent', showrecent)],
        states={
            GETLISTNAME: [MessageHandler(filters.ALL, get_list_name)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    return handler
