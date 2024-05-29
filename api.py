from flask import Flask, request, jsonify
from dotenv import load_dotenv
from crewai import Crew, Process
from crew.agents import CustomAgents
from crew.tasks import CustomTasks
from crew.crew import generate_article

app = Flask(__name__)

# Load environment variables
load_dotenv()


@app.route("/generate-article", methods=["POST"])
def generate_article_endpoint():
    data = request.json

    if not data:
        return jsonify({"error": "No data provided"}), 400

    topic = data.get("topic")
    language = data.get("language", "FR")

    if not topic:
        return jsonify({"error": "Topic is required"}), 400

    try:
        article = generate_article(topic=topic, language=language)
        return jsonify({"article": article})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    from os import environ

    port = int(environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
