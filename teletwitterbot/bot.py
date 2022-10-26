from telegram.ext import ApplicationBuilder, CommandHandler

from teletwitterbot import commands
from teletwitterbot.config import environment, settings


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

    if environment == "production":
        webhook_url = f'https://{settings["domain"]}:8443/{settings["BOT_TOKEN"]}'
        application.bot.setWebhook(webhook_url,
                                   certificate=settings["cert_path"])
        application.run_webhook(listen="0.0.0.0",
                                port=8443,
                                url_path=settings["BOT_TOKEN"],
                                key=settings["private_key_path"],
                                cert=settings["cert_path"],
                                webhook_url=webhook_url)
    else:
        application.bot.deleteWebhook()
        application.run_polling()
