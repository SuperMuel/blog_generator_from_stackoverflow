from crewai_tools import BaseTool
from pydantic.v1 import BaseModel, Field
from typing import Optional, Type, Any
import requests
from json import loads
from datetime import datetime


class StackOverflowAnswerToolSchema(BaseModel):
    """Input for StackOverflowAnswerTool."""

    answer_id: str = Field(..., description="Mandatory answer ID to search for.")


class StackOverflowAnswerTool(
    BaseTool
):  # TODO: also check https://python.langchain.com/v0.1/docs/integrations/tools/stackexchange/
    name: str = "Get answer from Stack Overflow"
    description: str = "Gets the answer from Stack Overflow for a given answer ID."
    args_schema: Type[BaseModel] = StackOverflowAnswerToolSchema

    def _run(self, **kwargs) -> str:  # type: ignore
        answer_id = kwargs.get("answer_id")
        if not answer_id:
            return "No answer ID provided."

        url = f"https://api.stackexchange.com/2.3/answers/{answer_id}?site=stackoverflow&filter=!*Mg4Pjg.VeqYI.wE"

        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.RequestException as e:
            return f"Failed to get answer from Stack Overflow. Error: {e}"

        items = loads(response.text).get("items")
        if not items:
            return "No answer found for the provided ID."

        item = items[0]

        # Extract the answer content
        #  "is_accepted":false,
        #  "score":4,
        #  "last_activity_date":1222199887,
        #  "creation_date":1222199887,
        #  "answer_id":123456,
        #  "question_id":120001,
        #  "content_license":"CC BY-SA 2.5",
        #  "body_markdown":"Another way to do Excel -&gt; CSV -&gt; Oracle is using External Tables, first introduced in 9i.  External tables let you query a flat file as if it&#39;s a table.  Behind the scenes Oracle is still using SQL*Loader.  There&#39;s a solid tutorial here:\r\n\r\nhttp://www.orafaq.com/node/848",
        #  "link":"https://stackoverflow.com/questions/120001/load-excel-data-sheet-to-oracle-database/123456#123456",
        #  "title":"Load Excel data sheet to Oracle database"

        # Extract the answer content
        answer = item.get("body_markdown")
        title = item.get("title")
        link = item.get("link")
        last_activity_date = item.get("last_activity_date")

        text = ""

        if title:
            text += f"Question title: {title}\n"

        if link:
            text += f"Answer Link: {link}\n"

        if last_activity_date:
            # Convert the timestamp to a datetime object
            last_activity_date = datetime.fromtimestamp(last_activity_date)
            now = datetime.now()
            time_diff = now - last_activity_date

            text += f"Last Activity: {time_diff.days} days ago\n"

        if answer:
            text += f"------------------Answer---------------------:\n{answer}\n\n-------------------------------------------------"

        return text


if __name__ == "__main__":
    tool = StackOverflowAnswerTool()
    print(tool.run(answer_id="30810322"))
