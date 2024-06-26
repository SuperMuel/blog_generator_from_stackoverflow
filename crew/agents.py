from crewai import Agent
from crewai_tools import SerperDevTool
from crew.tools import SearchStackOverflowTool, StackOverflowAnswerTool


class CustomAgents:
    """Custom agents for the crew."""

    def __init__(self, default_llm):
        self.default_llm = default_llm
        self.search_stackoverflow_tool = SearchStackOverflowTool()  # type: ignore
        self.get_stackoverflow_answer = StackOverflowAnswerTool()

    def stackoverflow_search_agent(self, llm=None):
        """Agent that searches Stack Overflow for relevant posts related to a topic."""
        return Agent(
            role="Search Agent",
            goal='Find relevant Stack Overflow posts related to "{topic}"',
            verbose=True,
            memory=True,
            backstory=(
                "As a diligent researcher, you are tasked with finding the best Stack Overflow "
                "posts related to the topic. Your expertise lies in identifying valuable information from search results."
            ),
            tools=[self.search_stackoverflow_tool],
            allow_delegation=False,
            llm=self.default_llm if llm is None else llm,
        )

    def stackoverflow_report_agent(
        self,
        llm=None,
    ):  # TODO : this do not take into account the question but only the answers. It should be improved, as questions can provide valuable information on the difficulty of the topic.
        """Agent that creates a detailed technical report from Stack Overflow answers."""
        return Agent(
            role="Report Agent",
            goal='Create a detailed technical report from Stack Overflow answers for "{topic}"',
            verbose=True,
            memory=True,
            backstory=(
                "As an expert in analyzing technical content, you are responsible for extracting "
                "the key points and solutions from the best Stack Overflow answers. Your goal is to create "
                "a detailed technical report that captures all important information and technical details."
            ),
            tools=[self.get_stackoverflow_answer],
            allow_delegation=False,
            llm=self.default_llm if llm is None else llm,
        )

    def reliable_sources_agent(self, llm=None):
        """Agent that finds reliable sources related to a topic for further reading."""
        return Agent(
            role="Reliable Sources Agent",
            goal='Find reliable sources related to "{topic}" for further reading',
            verbose=True,
            memory=True,
            backstory=(
                "As a seasoned researcher, your expertise lies in identifying the most authoritative and reliable sources "
                "for technical topics. Your mission is to find the best resources to recommend for further reading."
                "You prefer to answer that you din't find any reliable sources than to provide unreliable ones."
                "You know how to identify outdated sources and won't include them in your recommendations."
                "You know that your personal knowledge is not enough to provide reliable sources, so you ALWAYS rely on the tools and context provided."
            ),
            tools=[SerperDevTool()],
            allow_delegation=False,
            llm=self.default_llm if llm is None else llm,
        )

    def blog_writer_agent(self, llm=None):
        """Agent that writes a detailed blog post based on the previous results and eventual feedback."""
        return Agent(
            role="Blog Writer",
            goal='Write a detailed blog post on "{topic}" based on the previous results.',
            verbose=True,
            memory=True,
            backstory=(
                "With a talent for creating engaging and informative content, you will write a comprehensive blog post "
                "that highlights the key points and solutions. "
                "You understand that the readers are beginners and need a detailed explanation of the topic. "
                "You are a native speaker of {language} language and can write in markdown format. "
                "You know how to apply feedback you receive on the topic and use your personal knowledge to make the necessary revisions."
                "Metaphors are great for explaining a complicated subject."
                "Here's the context of the user/company requesting the article : "
                "<context>"
                "{context}"
                "</context> You can use this information to tailor the blog post to the user's needs."
                # TODO : define the tone, style and structure of the blog post
            ),
            tools=[],
            allow_delegation=False,
            llm=self.default_llm if llm is None else llm,
        )

    def evaluator_agent(self, llm=None):
        """Agent that evaluates the quality of the blog post and provides feedback."""
        return Agent(
            role="Evaluator Agent",
            goal="Evaluate the quality of the blog post based on readability, accuracy, relevance, and overall quality. Provide constructive feedback for revisions.",
            verbose=True,
            memory=True,
            backstory=(
                "As an experienced editor, you excel at evaluating technical content and providing constructive feedback to enhance readability, accuracy, and overall quality. "
                "You are a native speaker of {language} and you provide feedback in this language. "
            ),
            tools=[],
            allow_delegation=False,
            llm=self.default_llm if llm is None else llm,
        )

    def internal_linking_agent(self, llm=None):
        """Agent that links existing articles within the new article."""
        return Agent(
            role="Linking Agent",
            goal='Add relevant links to existing articles within the new article "{topic}".',
            verbose=True,
            memory=True,
            backstory=(
                "As an expert in creating interconnected content, you will identify opportunities to link to other relevant articles "
                "to enhance the new article. Your goal is to find meaningful connections and improve the reader's experience by providing "
                "additional resources. You understand that it's better to leave the article without links than to include irrelevant ones."
            ),
            tools=[],
            allow_delegation=False,
            llm=self.default_llm if llm is None else llm,
        )
