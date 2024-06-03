from dotenv import load_dotenv
from crew import generate_article
import agentops


def main():
    load_dotenv()

    # Define your topic and language
    DEFAULT_TOPIC = "How do I delete a Git branch locally and remotely?"
    LANGUAGE = "French"

    topic = input(f"Enter the topic, or press enter to use default ({DEFAULT_TOPIC}): ")

    if not topic:
        topic = DEFAULT_TOPIC

    agentops.init()

    try:
        article = generate_article(topic=topic, language=LANGUAGE)
        print(article)
    # except ctrl+c
    except KeyboardInterrupt:
        agentops.end_session("Fail", end_state_reason="User Interrupted")
        return
    except Exception as e:
        print(f"Error generating article: {e}")
        agentops.end_session("Fail", end_state_reason=str(e))
        return

    agentops.end_session("Success")


if __name__ == "__main__":
    main()
