import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from google.cloud import dialogflow_v2 as dialogflow
from logger_config import configure_logger
from dialogflow_api import detect_intent


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Здравствуйте")


def handle_message(update: Update, context: CallbackContext):
    user_text = update.message.text
    chat_id = str(update.message.chat_id)

    try:
        reply = detect_intent(project_id, chat_id, user_text).fulfillment_text
        update.message.reply_text(reply)
    except Exception:
        logging.exception(f"Ошибка при обращении к DialogFlow")


def main():
    load_dotenv()
    telegram_token = os.getenv("TELEGRAM_TOKEN")
    tg_chat_id = os.getenv("TG_CHAT_ID")
    global project_id
    project_id = os.getenv("PROJECT_ID")

    configure_logger(telegram_token, tg_chat_id)

    updater = Updater(telegram_token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()