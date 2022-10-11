from telegram.ext import ApplicationBuilder, CommandHandler

from teletwitterbot import commands
from teletwitterbot.config import settings


def main():
    builder = ApplicationBuilder().token(settings["BOT_TOKEN"])
    if settings["proxy_url"]:
        builder.proxy_url(settings["proxy_url"])
        builder.get_updates_proxy_url(settings["proxy_url"])
    application = builder.build()

    start_handler = CommandHandler('start', commands.start)
    application.add_handler(start_handler)

    createlist_handler = CommandHandler('createlist', commands.createlist)
    application.add_handler(createlist_handler)

    addtolist_handler = CommandHandler('addtolist', commands.addtolist)
    application.add_handler(addtolist_handler)

    showrecent_handler = CommandHandler('showrecent', commands.showrecent)
    application.add_handler(showrecent_handler)

    application.run_polling()
