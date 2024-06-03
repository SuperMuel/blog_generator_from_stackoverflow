from crewai import Crew, Process
from .agents import CustomAgents
from .tasks import CustomTasks

from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic


def generate_article(topic: str, language: str = "FR") -> str:
    claude3_sonnet = ChatAnthropic(model_name="claude-3-sonnet-20240229", max_tokens=4096)  # type: ignore
    gpt4o = ChatOpenAI(model_name="gpt-4o", max_tokens=4096)  # type: ignore

    # Initialize custom agents and tasks
    agents = CustomAgents(default_llm=gpt4o)
    tasks = CustomTasks()

    # Create agents
    search_agent = agents.stackoverflow_search_agent()
    report_agent = agents.stackoverflow_report_agent()
    reliable_sources_agent = agents.reliable_sources_agent()
    writer_agent = agents.blog_writer_agent()
    evaluator_agent = agents.evaluator_agent()

    # Create tasks
    search_task = tasks.search_stackoverflow_task(search_agent)
    report_task = tasks.generate_stackoverflow_technical_report(report_agent)
    reliable_sources_task = tasks.find_reliable_sources_task(
        reliable_sources_agent, topic
    )
    write_task = tasks.write_task(
        writer_agent,
        topic,
        language,
        context_tasks=[report_task, reliable_sources_task],
    )
    evaluation_task = tasks.evaluation_task(evaluator_agent, context_tasks=[write_task])
    revision_task = tasks.revision_task(
        writer_agent,
        [
            reliable_sources_task,
            write_task,
            evaluation_task,
        ],
        topic,
        language,
    )

    # Define your crew
    crew = Crew(
        agents=[
            search_agent,
            report_agent,
            reliable_sources_agent,
            writer_agent,
            evaluator_agent,
        ],
        tasks=[
            search_task,
            report_task,
            reliable_sources_task,
            write_task,
            evaluation_task,
            revision_task,
        ],
        process=Process.sequential,
    )

    # Kickoff the crew
    return crew.kickoff(inputs={"topic": topic, "language": language})
