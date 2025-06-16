import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from google.cloud import dialogflow_v2 as dialogflow


load_dotenv()


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

PROJECT_ID = os.getenv("PROJECT_ID")


def detect_intent_text(project_id, session_id, text, language_code="ru"):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    return response.query_result.fulfillment_text


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Здравствуйте")


def handle_message(update: Update, context: CallbackContext):
    user_text = update.message.text
    chat_id = str(update.message.chat_id)

    try:
        reply = detect_intent_text(PROJECT_ID, chat_id, user_text)
        update.message.reply_text(reply)
    except Exception as e:
        logging.error(f"Ошибка при обращении к DialogFlow: {e}")
        update.message.reply_text("Произошла ошибка при обработке. Попробуй ещё раз.")


def main():
    updater = Updater("8026982807:AAGVWzX3K7hkgL3q-wXDMoD5fhBL5cMWVmc")
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()