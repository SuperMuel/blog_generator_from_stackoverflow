from dotenv import load_dotenv

from crewai import Agent, Task, Crew, Process
from tools import SearchStackOverflowTool, StackOverflowAnswerTool
from langchain_anthropic import ChatAnthropic
from datetime import datetime


load_dotenv()

claude3Sonnet = ChatAnthropic(model_name="claude-3-sonnet-20240229", max_tokens=4096)  # type: ignore

# Définir le topic global
TOPIC = "Comprendre les promesses en JavaScript"
LANGUAGE = "French"

search_stackoverflow_tool = SearchStackOverflowTool()

stackoverflow_search_agent = Agent(
    role="Search Agent",
    goal="Find relevant Stack Overflow posts related to {topic}",
    verbose=True,
    memory=True,
    backstory=(
        "As a diligent researcher, you are tasked with finding the best Stack Overflow "
        "posts related to the topic. Your expertise lies in identifying valuable information from search results."
    ),
    tools=[search_stackoverflow_tool],
    allow_delegation=False,
    llm=claude3Sonnet,
)


# Agent 2: stackoverflow_report_agent
get_stackoverflow_answer = StackOverflowAnswerTool()

stackoverflow_report_agent = Agent(
    role="Report Agent",
    goal="Create a detailed technical report from Stack Overflow answers for {topic}",
    verbose=True,
    memory=True,
    backstory=(
        "As an expert in analyzing technical content, you are responsible for extracting "
        "the key points and solutions from the best Stack Overflow answers. Your goal is to create "
        "a detailed technical report that captures all important information and technical details."
    ),
    tools=[get_stackoverflow_answer],
    allow_delegation=False,
    llm=claude3Sonnet,
)


# Agent 3: blog_writer_agent
blog_writer_agent = Agent(
    role="Blog Writer",
    goal="Write a detailed blog post on {topic} based on the previous results.",
    verbose=True,
    memory=True,
    backstory=(
        "With a talent for creating engaging and informative content, you will write a comprehensive blog post "
        "that highlights the key points and solutions. "
        "You understand that the readers are beginners and need a detailed explanation of the topic. "
        "You are a native speaker of {language} language and can write in markdown format. "
        # TODO : define the tone, style and structure of the blog post
    ),
    tools=[],
    allow_delegation=False,
    llm=claude3Sonnet,
)


# Tâche 1: Recherche et sélection de résultats Stack Overflow
search_task = Task(
    description=(
        "Use the SerperDev tool to search for Stack Overflow posts related to '{topic}'. "
        "Select between one and three relevant results and obtain the sitelinks for each result."
        "The url of an answer is in the format 'https://stackoverflow.com/a/<answer_id>'."
        "Even if the topic in a foreign language, you try to find the best answers from english posts because "
        "it's the most common language for programming. You don't need to translate your results."
    ),
    expected_output="A list of URLs of the best answers for each selected Stack Overflow post.",
    agent=stackoverflow_search_agent,
)

# Task: Creation of a detailed technical report
report_task = Task(
    description=(
        "Read the answers from the provided Stack Overflow URLs using the StackOverflowAnswerTool. "
        "Create a detailed technical report that focuses on common issues and technical details of the solutions. "
        "Ensure that no user-specific references or mentions of Stack Overflow are included. "
        "The report should be comprehensive and retain all significant information from the answers."
        "Include relevant code snippets and explanations in the report."
    ),
    expected_output="A detailed technical report highlighting key problems and solutions from the Stack Overflow answers.",
    agent=stackoverflow_report_agent,
)

# Tâche 3: Rédaction de l'article de blog
write_task = Task(
    description=(
        "Write a comprehensive blog post on {topic} based on the summaries of the selected Stack Overflow answers. "
        "Ensure the article is informative, engaging, and formatted in markdown. "
        "The blog post is targeted towards beginners. "
        "Language of the blog post should be {language}."
    ),
    expected_output="A markdown formatted blog post on {topic} in {language}.",
    agent=blog_writer_agent,
    output_file=f"blog_post_{TOPIC}_{LANGUAGE}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.md",
)


# Former la Crew avec les agents et tâches définis
crew = Crew(
    agents=[stackoverflow_search_agent, stackoverflow_report_agent, blog_writer_agent],
    tasks=[search_task, report_task, write_task],
    process=Process.sequential,
)

# Lancer le processus avec le topic défini
result = crew.kickoff(inputs={"topic": TOPIC, "language": LANGUAGE})
print(result)


# TODO: Ensure that the code blocks written can run without any errors, or that explanations are provided for any errors that may occur. For instance, imports should be correct, or functions and variables not defined should be explained.
# find subjects in the generated blog post that would benefit from a clarification. For instance, if the term "microtask" occurs in a blog on a javascript subject, it should be explained in a way that a beginner can understand, or removed and replaced with simpler terms.
# TODO : SEO optimization
# Add context, so that it doesn't write "Bienvenue sur ce blog dédié au développement Python ! "

# Add an evaluator agent. The evaluator agent will be responsible for evaluating the quality of the blog post based on predefined criteria. The criteria can include
# readability, accuracy, relevance, and overall quality of the content. If there are traductions, ensure that they are accurate, and coherent. If there are code snippets, ensure that the variables and functions names are all in the same language.
# The evaluator will provide feedback on what could be missing, what's could be improved, and what could be removed.
# The evaluator agent will provide feedback to the blog writer agent for any necessary revisions or improvements.
