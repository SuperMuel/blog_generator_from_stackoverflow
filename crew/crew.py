from crewai import Crew, Process
from agents import CustomAgents
from tasks import CustomTasks
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
    write_task = tasks.write_task(writer_agent, TOPIC, LANGUAGE)
    evaluation_task = tasks.evaluation_task(evaluator_agent, write_task)
    revision_task = tasks.revision_task(
        writer_agent, [write_task, evaluation_task], TOPIC, LANGUAGE
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
