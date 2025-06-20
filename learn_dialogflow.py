import json
import os
from dotenv import load_dotenv
from google.cloud import dialogflow_v2 as dialogflow, dialogflow_v2


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    client = dialogflow.IntentsClient()
    parent = dialogflow.AgentsClient.agent_path(project_id)

    training_phrases = []
    for phrase in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=phrase)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message]
    )

    response = client.create_intent(request={"parent": parent, "intent": intent})
    return response.display_name


def main():
    load_dotenv()
    project_id = os.getenv("PROJECT_ID")

    with open("questions.json", encoding="utf-8") as f:
        data = json.load(f)

    for intent_name, content in data.items():
        questions = content["questions"]
        answer = content["answer"]

        created_name = create_intent(
            project_id=project_id,
            display_name=intent_name,
            training_phrases_parts=questions,
            message_texts=[answer]
        )
        print(f"Intent created: {created_name}")


if __name__ == '__main__':
    main()

