import sys
import logging

from .config import LOG_LEVEL

LOG_LEVELS = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL,
}

logging.getLogger().setLevel(LOG_LEVELS.get(LOG_LEVEL, logging.INFO))

class Logger:
    msg = {
        "OPEN": "\033[30;42m", # Black foreground, Green background
        "OPEN_WATCH": "\033[37;41m", # White foreground, Red background
        "OPEN_PROCESS": "\033[30;43m", # Black foreground, Yellow background
        "CLOSE": "\033[0m" # Reset to default
    }

    def ok(self, message_label, message):
        logging.info(f'{self.msg["OPEN"]}{message_label}{self.msg["CLOSE"]}: {message}')

    def error(self, message_label, message):
        logging.error(f'{self.msg["OPEN_WATCH"]}{message_label}{self.msg["CLOSE"]}: {message}')

    def walk(self, message_label, message):
        logging.info(f'{self.msg["OPEN_PROCESS"]}{message_label}{self.msg["CLOSE"]}: {message}')

    def halt(self):
        self.error("Halting process...", "")
        sys.exit(1)

def main():
    logger = Logger()
    logger.ok("Everything is fine.", "")
    logger.error("An error has occurred.", "")
    logger.walk("Continuing process...", "")
    logger.halt()

if __name__ == "__main__":
    main()
