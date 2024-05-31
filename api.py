from flask import Flask, request, jsonify
from dotenv import load_dotenv
from crew import generate_article
import requests
import threading
import os
import logging

app = Flask(__name__)

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_article_and_callback(topic, language, callback_url, custom_args):
    try:
        logger.info(f"Generating article for topic: {topic} in language: {language}")
        article = generate_article(topic=topic, language=language)
        response = requests.post(
            callback_url,
            json={
                "article": article,
                "custom_args": custom_args,
            },
        )
        response.raise_for_status()
        logger.info(f"Successfully posted article to {callback_url}")
    except Exception as e:
        error_message = str(e)
        logger.error(f"Error generating article: {error_message}")
        requests.post(
            callback_url,
            json={
                "error": error_message,
                "custom_args": custom_args,
            },
        )


@app.route("/generate-article", methods=["POST"])
def generate_article_endpoint():
    data = request.json

    if not data:
        logger.warning("No data provided in the request")
        return jsonify({"error": "No data provided"}), 400

    topic = data.get("topic")
    language = data.get("language", "French")
    callback_url = data.get("callback_url")
    custom_args = data.get("custom_args", {})

    if not topic:
        logger.warning("Topic is required but not provided")
        return jsonify({"error": "Topic is required"}), 400

    if not callback_url:
        logger.warning("Callback URL is required but not provided")
        return jsonify({"error": "Callback URL is required"}), 400

    logger.info(f"Starting article generation for topic: {topic}")
    # Start the background thread
    thread = threading.Thread(
        target=generate_article_and_callback,
        args=(topic, language, callback_url, custom_args),
    )
    thread.start()

    logger.info("Article generation thread started")
    return jsonify({"message": "Article generation started"}), 202


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    logger.info(f"Starting Flask app on port {port}")
    app.run(host="0.0.0.0", port=port, debug=True)
