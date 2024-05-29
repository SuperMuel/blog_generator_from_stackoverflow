from crewai import Crew, Process
from crew.agents import CustomAgents
from crew.tasks import CustomTasks
from dotenv import load_dotenv


def generate_article(topic: str, language: str = "FR") -> str:

    # Initialize custom agents and tasks
    agents = CustomAgents()
    tasks = CustomTasks()

    # Create agents
    search_agent = agents.stackoverflow_search_agent()
    report_agent = agents.stackoverflow_report_agent()
    writer_agent = agents.blog_writer_agent()
    evaluator_agent = agents.evaluator_agent()

    # Create tasks
    search_task = tasks.search_task(search_agent)
    report_task = tasks.report_task(report_agent)
    write_task = tasks.write_task(writer_agent, topic, language)
    evaluation_task = tasks.evaluation_task(evaluator_agent, write_task)
    revision_task = tasks.revision_task(
        writer_agent, [write_task, evaluation_task], topic, language
    )

    # Define your crew
    crew = Crew(
        agents=[search_agent, report_agent, writer_agent, evaluator_agent],
        tasks=[search_task, report_task, write_task, evaluation_task, revision_task],
        process=Process.sequential,
    )

    # Kickoff the crew
    return crew.kickoff(inputs={"topic": topic, "language": language})


if __name__ == "__main__":
    load_dotenv()

    # Define your topic and language
    TOPIC = "La programmation asynchrone en Python"
    LANGUAGE = "French"

    article = generate_article(topic=TOPIC, language=LANGUAGE)

    print(article)


# TODO: Ensure that the code blocks written can run without any errors, or that explanations are provided for any errors that may occur. For instance, imports should be correct, or functions and variables not defined should be explained.
# find subjects in the generated blog post that would benefit from a clarification. For instance, if the term "microtask" occurs in a blog on a javascript subject, it should be explained in a way that a beginner can understand, or removed and replaced with simpler terms.
# TODO : SEO optimization
# Add context, so that it doesn't write "Bienvenue sur ce blog dédié au développement Python ! "
