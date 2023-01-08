
from telegram import Update
from telegram.ext import (CommandHandler, ContextTypes, ConversationHandler,
                          MessageHandler, filters)

from teletwitterbot.database import List, Member, session
from teletwitterbot.processes.commons import cancel

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


def get_handler():
    handler = ConversationHandler(
        entry_points=[CommandHandler('addmember', addmember)],
        states={
            GETLISTNAME: [MessageHandler(filters.ALL, get_list_name)],
            GETMEMBERUSERNAME: [MessageHandler(filters.ALL, get_member_username)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    return handler
