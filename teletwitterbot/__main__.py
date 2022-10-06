import logging

from teletwitterbot.bot import main

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG)

if __name__ == "__main__":
    main()
