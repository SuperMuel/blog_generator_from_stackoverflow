import argparse
import os
from datetime import datetime

from dotenv import load_dotenv
from pathvalidate import sanitize_filename

from crew import generate_article
from crew.ai_models import AIModel


def get_arguments():
    """Parse and return command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate and save an article based on a given topic."
    )
    parser.add_argument("topic", type=str, help="The topic for the article.")
    parser.add_argument(
        "-L",
        "--language",
        type=str,
        default="French",
        help="The language of the article (default: French).",
    )
    parser.add_argument(
        "-C",
        "--context",
        type=str,
        default="",
        help="Additional context to provide to the AI model.",
    )

    # TODO : add ai model choice
    return parser.parse_args()


def sanitize_title(title: str, topic: str) -> str:
    """Sanitize the title of the article."""
    sanitized_title = title.split("\n")[0].strip().strip("#").strip()
    if not sanitized_title:
        sanitized_title = topic
    return sanitize_filename(sanitized_title).replace(" ", "_")


def save_article(article: str, sanitized_title: str) -> str:
    """Save the article to a file and return the file path."""
    filename = f"{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}_{sanitized_title}.md"
    path = os.path.join("posts", filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        f.write(article)

    return path


def main():
    """Main function to generate and save the article."""
    args = get_arguments()

    llm = AIModel.GPT_4O_MINI.to_client()

    try:
        article = generate_article(
            llm=llm,
            topic=args.topic,
            language=args.language,
            context=args.context,
        )
        print(article)

        title = sanitize_title(article, args.topic)
        path = save_article(article, title)

        print(f"Article saved to {path}")

    except KeyboardInterrupt:
        print("Operation cancelled by user.")
    except Exception as e:
        print(f"Error generating article: {e}")

if __name__ == "__main__":
    load_dotenv()
    main()
