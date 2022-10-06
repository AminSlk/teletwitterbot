import os

Config = {
    "BOT_TOKEN": os.getenv("BOT_TOKEN"),
    "proxy_url": "socks5://127.0.0.1:1080",
    "db_path": "sqlite:///database.db"
}
