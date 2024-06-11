from pydantic import BaseModel, Field, UrlConstraints
from typing import Annotated, Optional, Dict

from pydantic_core import Url


HttpUrl = Annotated[
    Url,
    UrlConstraints(max_length=2083, allowed_schemes=["http", "https"]),
]


class ArticleGenerationRequest(BaseModel):
    topic: str = Field(
        ...,
        title="The topic of the article",
        examples=["Use of AI in healthcare"],
        min_length=5,
        max_length=1000,
    )
    language: Optional[str] = "French"
    callback_url: HttpUrl = Field(
        ...,
        title="The URL to send the article to, once it has been generated.",
        examples=["https://example.com/callback"],
    )
    custom_args: Optional[Dict] = Field(
        default_factory=dict,
        description="Custom arguments that will be returned in the callback response.",
        examples=[{"requestId": "1234"}],
    )


class ArticledGeneratedEvent(BaseModel):
    article: str = Field(
        ...,
        description="The generated article in markdown format.",
    )
    custom_args: Optional[Dict] = Field(
        default_factory=dict,
        description="Custom arguments that were passed in the initial request.",
        examples=[{"requestId": "1234"}],
    )


class ArticleGenerationStarted(BaseModel):
    ok: bool = True
