from dotenv import load_dotenv
from crew import generate_article

if __name__ == "__main__":
    load_dotenv()

    # Define your topic and language
    DEFAULT_TOPIC = "How do I delete a Git branch locally and remotely?"
    LANGUAGE = "French"

    topic = input(f"Enter the topic, or press enter to use default ({DEFAULT_TOPIC}): ")

    if not topic:
        topic = DEFAULT_TOPIC

    article = generate_article(topic=topic, language=LANGUAGE)

    print(article)
