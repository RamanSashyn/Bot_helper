import logging
from telegram import Bot


class TelegramLogsHandler(logging.Handler):
    def __init__(self, bot_token, chat_id):
        super().__init__()
        self.bot = Bot(token=bot_token)
        self.chat_id = chat_id

    def emit(self, record):
        log_entry = self.format(record)
        try:
            self.bot.send_message(chat_id=self.chat_id, text=log_entry)
        except Exception:
            pass


def configure_logger(bot_token, chat_id):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    handler = TelegramLogsHandler(bot_token, chat_id)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger
