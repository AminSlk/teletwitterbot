import os

from dynaconf import Dynaconf

settings = Dynaconf(envvar_prefix="DYNACONF",
                    settings_files=['settings.yaml', '.secrets.yaml'],
                    environments=True)
environment = os.environ['ENV_FOR_DYNACONF']
