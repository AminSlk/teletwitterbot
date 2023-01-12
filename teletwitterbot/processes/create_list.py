import datetime

from telegram import Update
from telegram.ext import (CommandHandler, ContextTypes, ConversationHandler,
                          MessageHandler, filters)

from teletwitterbot.database import List, session
from teletwitterbot.processes.commons import (cancel, name_filter,
                                              send_bad_name_message)

GETLISTNAME = range(1)

async def createlist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Please send the list name!")
    return GETLISTNAME

async def get_list_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    await send_bad_name_message(update, context)
    return GETLISTNAME


def get_handler():
    handler = ConversationHandler(
        entry_points=[CommandHandler('createlist', createlist)],
        states={
            GETLISTNAME: [MessageHandler(name_filter, get_list_name),
             MessageHandler(filters.ALL, bad_list_name)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    return handler
