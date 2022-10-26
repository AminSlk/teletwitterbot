import os

from dynaconf import Dynaconf

settings = Dynaconf(envvar_prefix="DYNACONF",
                    settings_files=['settings.yaml', '.secrets.yaml'],
                    environments=True)
environment = os.environ.get('ENV_FOR_DYNACONF', 'default')
WEBHOOK_URL = f'https://{settings.get("domain", "localhost")}:8443/{settings["BOT_TOKEN"]}'
