from telegram.ext import ApplicationBuilder, CommandHandler

from teletwitterbot.config import environment, settings
from teletwitterbot.processes import (add_member, commons, create_list,
                                      show_recent)


def main():
    builder = ApplicationBuilder().token(settings["BOT_TOKEN"])
    if settings["proxy_url"]:
        builder.proxy_url(settings["proxy_url"])
        builder.get_updates_proxy_url(settings["proxy_url"])
    application = builder.build()

    add_handlers(application)

    if environment == "production":
        application.run_webhook(
            listen="127.0.0.1",
            port=settings["local_port"],
            url_path=settings["BOT_TOKEN"],
            webhook_url=
            f'https://{settings["domain"]}:{settings["webhook_port"]}/{settings["BOT_TOKEN"]}'
        )
    else:
        application.run_polling()


def add_handlers(application):
    start_handler = CommandHandler('start', commons.start)
    application.add_handler(start_handler)

    application.add_handler(create_list.get_handler())
    application.add_handler(add_member.get_handler())
    application.add_handler(show_recent.get_handler())
