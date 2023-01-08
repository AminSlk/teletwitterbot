import datetime

from telegram import Update
from telegram.ext import (CommandHandler, ContextTypes, ConversationHandler,
                          MessageHandler, filters)

from teletwitterbot.database import List, session

GETLISTNAME = range(1)

async def createlist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Please send the list name!")
    return GETLISTNAME

async def getlistname(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot_list = List(name=update.message.text,
                    username=update.effective_user.username,
                    last_check=datetime.datetime.now() -
                    datetime.timedelta(days=1))
    session.add(bot_list)
    session.commit()
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"List {bot_list.name} Created!"
    )
    return ConversationHandler.END

async def bad_list_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="List name should only have alphanumeric and Underscore characters!\n\
            Please send another name!"
    )
    return GETLISTNAME

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Canceled!"
    )
    return ConversationHandler.END


def get_handler():
    handler = ConversationHandler(
        entry_points=[CommandHandler('createlist', createlist)],
        states={
            GETLISTNAME: [MessageHandler(filters.Regex("^[a-zA-Z0-9_]*$"), getlistname),
             MessageHandler(filters.ALL, bad_list_name)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    return handler
