from dotenv import load_dotenv

from crewai import Agent, Task, Crew, Process
from tools import SearchStackOverflowTool, StackOverflowAnswerTool
from langchain_anthropic import ChatAnthropic
from datetime import datetime


load_dotenv()

claude3Sonnet = ChatAnthropic(model_name="claude-3-sonnet-20240229", max_tokens=4096)  # type: ignore

# Définir le topic global
TOPIC = "Python Yield"
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

# Agent 2: stackoverflow_summary_agent
get_stackoverflow_answer = StackOverflowAnswerTool()

stackoverflow_summary_agent = Agent(
    role="Summary Agent",
    goal="Summarize Stack Overflow answers for {topic}",
    verbose=True,
    memory=True,
    backstory=(
        "As an expert in summarizing technical content, you are responsible for extracting "
        "the key points and solutions from the best Stack Overflow answers, while omitting "
        "any user-specific and stackoverflow references."
    ),
    # TODO : expected output.
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
        "Use the SerperDev tool to search for Stack Overflow posts related to {topic}. "
        "Select between one and three relevant results and obtain the sitelinks for each result."
        "The url of an answer is in the format 'https://stackoverflow.com/a/<answer_id>'."
    ),
    expected_output="A list of URLs of the best answers for each selected Stack Overflow post.",
    agent=stackoverflow_search_agent,
)

# Tâche 2: Lecture et résumé des réponses de Stack Overflow

# TODO : this is not actually a summary. Because it shortens the text too much and looses a lot of information.
# it should be more like a detailed summary, or a rephrasing of the answer.
#! Or better : "techical report on the answers"
summary_task = Task(
    description=(
        "Read the answers from the provided Stack Overflow URLs using the StackOverflowAnswerTool. "  # TODO : check tool name
        "Summarize the answers by focusing on common issues and technical details of the solutions. "
        "Exclude any user-specific references and mentions of Stack Overflow."
    ),
    expected_output="A summarized report of the answers highlighting key problems and solutions.",
    agent=stackoverflow_summary_agent,
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
    agents=[stackoverflow_search_agent, stackoverflow_summary_agent, blog_writer_agent],
    tasks=[search_task, summary_task, write_task],
    process=Process.sequential,  # Exécution séquentielle des tâches
)

# Lancer le processus avec le topic défini
result = crew.kickoff(inputs={"topic": TOPIC, "language": LANGUAGE})
print(result)


# TODO: Ensure that the code blocks written can run without any errors, or that explanations are provided for any errors that may occur. For instance, imports should be correct, or functions and variables not defined should be explained.

# TODO : SEO optimization
# Add context, so that it doesn't write "Bienvenue sur ce blog dédié au développement Python ! "
