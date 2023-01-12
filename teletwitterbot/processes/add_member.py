
from telegram import Update
from telegram.ext import (CommandHandler, ContextTypes, ConversationHandler,
                          MessageHandler, filters)

from teletwitterbot.database import List, Member, session
from teletwitterbot.processes.commons import (cancel, name_filter,
                                              send_bad_name_message)

GETLISTNAME, GETMEMBERUSERNAME = range(2)

async def addmember(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Please send the list name to add member to!")
    return GETLISTNAME

async def get_list_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    list_name = update.message.text
    context.user_data['list'] = list_name
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Now please send the twitter username of the member you want to add to your list"
    )
    return GETMEMBERUSERNAME

async def get_member_username(update: Update, context: ContextTypes.DEFAULT_TYPE):
    member_username = update.message.text
    bot_list = session.query(List).filter_by(
        name=context.user_data['list'], username=update.effective_user.username).one()
    member = Member(list=bot_list, username=member_username)
    session.add(member)
    session.commit()
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Member {member.username} added to list {member.list.name}")
    return ConversationHandler.END

async def bad_list_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_bad_name_message(update, context)
    return GETLISTNAME

async def bad_member_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_bad_name_message(update, context)
    return GETMEMBERUSERNAME

def get_handler():
    handler = ConversationHandler(
        entry_points=[CommandHandler('addmember', addmember)],
        states={
            GETLISTNAME: [MessageHandler(name_filter, get_list_name),
            MessageHandler(filters.ALL, bad_list_name)],
            GETMEMBERUSERNAME: [MessageHandler(name_filter, get_member_username),
            MessageHandler(filters.ALL, bad_member_name)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    return handler
