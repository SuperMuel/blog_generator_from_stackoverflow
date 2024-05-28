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
        "You know how to apply feedback you receive on the topic and use your personal knowledge to make the necessary revisions."
        "Metaphors are great for explaining a complicated subject."
        # TODO : define the tone, style and structure of the blog post
    ),
    tools=[],
    allow_delegation=False,
    llm=claude3Sonnet,
)

evaluator_agent = Agent(
    role="Evaluator Agent",
    goal="Evaluate the quality of the blog post based on readability, accuracy, relevance, and overall quality. Provide constructive feedback for revisions.",
    verbose=True,
    memory=True,
    backstory=(
        "As an experienced editor, you excel at evaluating technical content and providing constructive feedback to enhance readability, accuracy, and overall quality."
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
        "Examples are better than theory, so include code snippets and practical examples. "
        "Language of the blog post should be {language}."
    ),
    expected_output="A markdown formatted blog post on {topic} in {language}.",
    agent=blog_writer_agent,
    output_file=f"blog_post_{TOPIC}_{LANGUAGE}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.md",  # todo delete that
)

evaluation_task = Task(
    description=(
        "Evaluate the blog post generated by the Blog Writer Agent. Assess the content for readability, accuracy, relevance, and overall quality. "
        "Ensure that translations are accurate and coherent, and that code snippets have consistent variable and function names, in the same language. "
        "Provide detailed feedback on what could be improved, what might be missing, and any elements that could be removed. "
    ),
    expected_output="A detailed feedback report.",
    agent=evaluator_agent,
    context=[write_task],
)


revision_task = Task(
    description=(
        "Read the blog post written and the subsequent evaluation feedback. Make necessary revisions based on the feedback provided. "
        "Ensure that all suggested improvements are implemented and that the blog post is polished and ready for publication."
    ),
    expected_output="A revised markdown formatted blog post on {topic} in {language}. ",
    agent=blog_writer_agent,
    context=[write_task, evaluation_task],
    output_file=f"revised_blog_post_{TOPIC}_{LANGUAGE}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.md",
)


crew = Crew(
    agents=[
        stackoverflow_search_agent,
        stackoverflow_report_agent,
        blog_writer_agent,
        evaluator_agent,
    ],
    tasks=[search_task, report_task, write_task, evaluation_task, revision_task],
    process=Process.sequential,
)

# Lancer le processus avec le topic défini
result = crew.kickoff(inputs={"topic": TOPIC, "language": LANGUAGE})
print(result)


# TODO: Ensure that the code blocks written can run without any errors, or that explanations are provided for any errors that may occur. For instance, imports should be correct, or functions and variables not defined should be explained.
# find subjects in the generated blog post that would benefit from a clarification. For instance, if the term "microtask" occurs in a blog on a javascript subject, it should be explained in a way that a beginner can understand, or removed and replaced with simpler terms.
# TODO : SEO optimization
# Add context, so that it doesn't write "Bienvenue sur ce blog dédié au développement Python ! "
