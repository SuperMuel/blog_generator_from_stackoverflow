from dotenv import load_dotenv
from crew import generate_article

if __name__ == "__main__":
    load_dotenv()

    # Define your topic and language
    TOPIC = "How do I delete a Git branch locally and remotely?"
    LANGUAGE = "French"

    article = generate_article(topic=TOPIC, language=LANGUAGE)

    print(article)
