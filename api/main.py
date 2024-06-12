from fastapi import APIRouter, FastAPI, BackgroundTasks
from dotenv import load_dotenv
from api.models import (
    ArticleGenerationRequest,
    ArticleGenerationStarted,
    ArticledGeneratedEvent,
)
import crew
import requests
import logging

from crew.ai_models import AIModel


# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# TODO : async this
def generate_article_and_callback(topic, language, callback_url, custom_args) -> None:
    try:
        logger.info(f"Generating article for topic: {topic} in language: {language}")
        article = crew.generate_article(
            llm=AIModel.CLAUDE_3_SONNET.to_client(),  # TODO : add choice
            topic=topic,
            language=language,
        )
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


# TODO :check https://fastapi.tiangolo.com/advanced/openapi-callbacks/


app = FastAPI(
    title="Article Generation API",
    version="0.1.0",
    description="API to generate articles using CrewAI and results from StackOverflow.",
)


generated_articles_callback_router = APIRouter()


@generated_articles_callback_router.post(
    "{$callback_url}",
)
def article_generated_notification(body: ArticledGeneratedEvent):
    pass


@app.post(
    "/generate-article",
    response_model=ArticleGenerationStarted,
    description="Triggers the generation of an article for a given topic, and sends the result to a callback URL.",
    status_code=202,
    callbacks=generated_articles_callback_router.routes,
)
def generate_article(
    article_request: ArticleGenerationRequest,
    background_tasks: BackgroundTasks,
):
    logger.info(f"Starting article generation for topic: {article_request.topic}")

    background_tasks.add_task(
        generate_article_and_callback,
        topic=article_request.topic,
        language=article_request.language,
        callback_url=article_request.callback_url,
        custom_args=article_request.custom_args,
    )

    return ArticleGenerationStarted()


@app.get("/", include_in_schema=False)
def read_root():
    return {"Hello": "World"}
