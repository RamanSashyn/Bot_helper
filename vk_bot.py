import os
import random
import logging
from dotenv import load_dotenv
from google.cloud import dialogflow_v2 as dialogflow
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from logger_config import configure_logger


def detect_intent_texts(project_id, session_id, text, language_code="ru"):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    return response.query_result


def main():
    load_dotenv()

    vk_token = os.getenv("VK_API_TOKEN")
    project_id = os.getenv("PROJECT_ID")
    tg_token = os.getenv("TELEGRAM_TOKEN")
    tg_chat_id = os.getenv("TG_CHAT_ID")

    configure_logger(tg_token, tg_chat_id)
    logger = logging.getLogger(__name__)
    logger.info("VK бот запускается...")

    try:
        vk_session = vk_api.VkApi(token=vk_token)
        vk_api_instance = vk_session.get_api()
        longpoll = VkLongPoll(vk_session, preload_messages=True)

        logger.info("VK бот успешно запущен и слушает сообщения")

        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                user_id = event.user_id
                text = event.text

                try:
                    dialogflow_response = detect_intent_texts(project_id, user_id, text)
                    if dialogflow_response.intent.is_fallback:
                        logger.info(f"FALLBACK: '{text}' от {user_id}")
                        continue

                    vk_api_instance.messages.send(
                        user_id=user_id,
                        message=dialogflow_response.fulfillment_text,
                        random_id=random.randint(1, 100000)
                    )
                    logger.info(f"Ответ отправлен пользователю {user_id}")

                except Exception as error:
                    logger.exception(f"Ошибка при обработке сообщения от {user_id}: {error}")

    except Exception as startup_error:
        logger.exception(f"Ошибка при запуске VK бота: {startup_error}")


if __name__ == "__main__":
    main()