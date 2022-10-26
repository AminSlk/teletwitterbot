from telegram.ext import ApplicationBuilder, CommandHandler

from teletwitterbot import commands
from teletwitterbot.config import WEBHOOK_URL, environment, settings


async def setup():
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

    if environment == "production":
        await application.bot.setWebhook(WEBHOOK_URL,
                                         certificate=settings["cert_path"])
    else:
        await application.bot.deleteWebhook()
    return application


def run(application):
    if environment == "production":
        application.run_webhook(listen="0.0.0.0",
                                port=8443,
                                url_path=settings["BOT_TOKEN"],
                                key=settings["private_key_path"],
                                cert=settings["cert_path"],
                                webhook_url=WEBHOOK_URL)
    else:
        application.run_polling()
