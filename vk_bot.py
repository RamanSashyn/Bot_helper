import os
import random

from dotenv import load_dotenv
from google.cloud import dialogflow_v2 as dialogflow
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType


def detect_intent_texts(project_id, session_id, text, language_code="ru"):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    return response.query_result


if __name__ == "__main__":
    load_dotenv()

    VK_API_TOKEN = os.getenv("VK_API_TOKEN")
    PROJECT_ID = os.getenv("PROJECT_ID")

    vk_session = vk_api.VkApi(token=VK_API_TOKEN)
    vk_api_instance = vk_session.get_api()
    longpoll = VkLongPoll(vk_session, preload_messages=True)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            result = detect_intent_texts(
                project_id=PROJECT_ID,
                session_id=event.user_id,
                text=event.text
            )

            if result.intent.is_fallback:
                continue

            vk_api_instance.messages.send(
                user_id=event.user_id,
                message=result.fulfillment_text,
                random_id=random.randint(1, 1000),
            )
