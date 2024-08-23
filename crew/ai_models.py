from enum import Enum
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic


class AIModel(Enum):
    CLAUDE_35_SONNET = "claude-3-5-sonnet-20240620"
    GPT_4O = "gpt-4o"
    GPT_4O_MINI = "gpt-4o-mini"
    CLAUDE_3_HAIKU = "claude-3-haiku-20240307"

    def to_client(
        self,
        max_tokens: int = 4096,
        max_retries: int = 20,
    ) -> BaseChatModel:
        match self:
            case AIModel.GPT_4O_MINI:
                return ChatOpenAI(
                    model_name=self.value,  # type: ignore
                    max_tokens=max_tokens,
                    max_retries=max_retries,
                )
            case AIModel.CLAUDE_35_SONNET:
                return ChatAnthropic(
                    model_name=self.value,
                    max_tokens=max_tokens,  # type: ignore
                    max_retries=max_retries,
                )
            case AIModel.CLAUDE_3_HAIKU:
                return ChatAnthropic(
                    model_name=self.value,
                    max_tokens=max_tokens,  # type: ignore
                    max_retries=max_retries,
                )

            case AIModel.GPT_4O:
                return ChatOpenAI(
                    model_name=self.value,  # type: ignore
                    max_tokens=max_tokens,
                    max_retries=max_retries,
                )
