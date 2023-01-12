
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler, filters

name_filter = filters.Regex("^[a-zA-Z0-9_]*$")


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Canceled!"
    )
    return ConversationHandler.END

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Welcome to TeleTwitter Bot!")

async def send_bad_name_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Name should only have alphanumeric and Underscore characters!\n\
            Please send another name!"
    )
