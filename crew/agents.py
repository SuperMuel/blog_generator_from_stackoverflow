from crewai import Agent
from langchain_anthropic import ChatAnthropic
from crew.tools import SearchStackOverflowTool, StackOverflowAnswerTool
from crewai_tools import SerperDevTool


class CustomAgents:
    """Custom agents for the crew."""

    def __init__(self):
        self.claude3Sonnet = ChatAnthropic(model_name="claude-3-sonnet-20240229", max_tokens=4096)  # type: ignore
        self.search_stackoverflow_tool = SearchStackOverflowTool()  # type: ignore
        self.get_stackoverflow_answer = StackOverflowAnswerTool()

    def stackoverflow_search_agent(self):
        """Agent that searches Stack Overflow for relevant posts related to a topic."""
        return Agent(
            role="Search Agent",
            goal="Find relevant Stack Overflow posts related to {topic}",
            verbose=True,
            memory=True,
            backstory=(
                "As a diligent researcher, you are tasked with finding the best Stack Overflow "
                "posts related to the topic. Your expertise lies in identifying valuable information from search results."
            ),
            tools=[self.search_stackoverflow_tool],
            allow_delegation=False,
            llm=self.claude3Sonnet,
        )

    def stackoverflow_report_agent(
        self,
    ):  # TODO : this do not take into account the question but only the answers. It should be improved, as questions can provide valuable information on the difficulty of the topic.
        """Agent that creates a detailed technical report from Stack Overflow answers."""
        return Agent(
            role="Report Agent",
            goal="Create a detailed technical report from Stack Overflow answers for {topic}",
            verbose=True,
            memory=True,
            backstory=(
                "As an expert in analyzing technical content, you are responsible for extracting "
                "the key points and solutions from the best Stack Overflow answers. Your goal is to create "
                "a detailed technical report that captures all important information and technical details."
            ),
            tools=[self.get_stackoverflow_answer],
            allow_delegation=False,
            llm=self.claude3Sonnet,
        )

    def reliable_sources_agent(self):
        """Agent that finds reliable sources related to a topic for further reading."""
        return Agent(
            role="Reliable Sources Agent",
            goal="Find reliable sources related to {topic} for further reading",
            verbose=True,
            memory=True,
            backstory=(
                "As a seasoned researcher, your expertise lies in identifying the most authoritative and reliable sources "
                "for technical topics. Your mission is to find the best resources to recommend for further reading."
                "You prefer to answer that you din't find any reliable sources than to provide unreliable ones."
            ),
            tools=[SerperDevTool()],
            allow_delegation=False,
            llm=self.claude3Sonnet,
        )

    def blog_writer_agent(self):
        """Agent that writes a detailed blog post based on the previous results and eventual feedback."""
        return Agent(
            role="Blog Writer",
            goal="Write a detailed blog post on {topic} based on the previous results.",
            verbose=True,
            memory=True,
            backstory=(
                "With a talent for creating engaging and informative content, you will write a comprehensive blog post "
                "that highlights the key points and solutions. "
                "You understand that the readers are beginners and need a detailed explanation of the topic. "
                "You are a native speaker of {language} language and can write in markdown format. "
                "You know how to apply feedback you receive on the topic and use your personal knowledge to make the necessary revisions."
                "Metaphors are great for explaining a complicated subject."
                # TODO : define the tone, style and structure of the blog post
            ),
            tools=[],
            allow_delegation=False,
            llm=self.claude3Sonnet,
        )

    def evaluator_agent(self):
        """Agent that evaluates the quality of the blog post and provides feedback."""
        return Agent(
            role="Evaluator Agent",
            goal="Evaluate the quality of the blog post based on readability, accuracy, relevance, and overall quality. Provide constructive feedback for revisions.",
            verbose=True,
            memory=True,
            backstory=(
                "As an experienced editor, you excel at evaluating technical content and providing constructive feedback to enhance readability, accuracy, and overall quality."
            ),
            tools=[],
            allow_delegation=False,
            llm=self.claude3Sonnet,
        )
