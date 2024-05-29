from flask import Flask, request, jsonify
from dotenv import load_dotenv
from crew.crew import generate_article
import requests
import threading
import os

app = Flask(__name__)

# Load environment variables
load_dotenv()


def generate_article_and_callback(topic, language, callback_url):
    try:
        article = generate_article(topic=topic, language=language)
        response = requests.post(callback_url, json={"article": article})
        response.raise_for_status()
    except Exception as e:
        error_message = str(e)
        requests.post(callback_url, json={"error": error_message})


@app.route("/generate-article", methods=["POST"])
def generate_article_endpoint():
    data = request.json

    if not data:
        return jsonify({"error": "No data provided"}), 400

    topic = data.get("topic")
    language = data.get("language", "French")
    callback_url = data.get("callback_url")

    if not topic:
        return jsonify({"error": "Topic is required"}), 400

    if not callback_url:
        return jsonify({"error": "Callback URL is required"}), 400

    # Start the background thread
    thread = threading.Thread(
        target=generate_article_and_callback, args=(topic, language, callback_url)
    )
    thread.start()

    return jsonify({"message": "Article generation started"}), 202


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
