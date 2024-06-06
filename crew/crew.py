from typing import Dict, List
from crewai import Crew, Process, Task, Agent
from langchain_anthropic import ChatAnthropic
from langsmith import traceable


from .agents import CustomAgents
from .tasks import CustomTasks


@traceable
def generate_article(
    topic: str,
    language: str = "FR",
    existing_articles: List[Dict] | None = None,
) -> str:
    # claude3_haiku = ChatAnthropic(model_name="claude-3-haiku-20240307", max_tokens=4096)  # type: ignore

    claude3_sonnet = ChatAnthropic(
        model_name="claude-3-sonnet-20240229",
        max_tokens=4096,  # type: ignore
    )

    # gpt4o = ChatOpenAI(model_name="gpt-4o", max_tokens=4096)  # type: ignore

    # Initialize custom agents and tasks
    agents = CustomAgents(default_llm=claude3_sonnet)
    tasks = CustomTasks()

    # Create agents
    search_agent = agents.stackoverflow_search_agent()
    report_agent = agents.stackoverflow_report_agent()
    reliable_sources_agent = agents.reliable_sources_agent()
    writer_agent = agents.blog_writer_agent()
    evaluator_agent = agents.evaluator_agent()
    internal_linking_agent = agents.internal_linking_agent()

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

    internal_linking_task = (
        tasks.link_existing_articles_task(
            internal_linking_agent,
            existing_articles,
        )
        if existing_articles is not None and len(existing_articles) > 0
        else None
    )

    agents_list: List[Agent] = [
        search_agent,
        report_agent,
        reliable_sources_agent,
        writer_agent,
        evaluator_agent,
        internal_linking_agent,
    ]

    tasks_list: List[Task] = [
        search_task,
        report_task,
        reliable_sources_task,
        write_task,
        evaluation_task,
        revision_task,
    ]

    if internal_linking_task is not None:
        tasks_list.append(internal_linking_task)

    # Define your crew
    crew = Crew(
        agents=agents_list,
        tasks=tasks_list,
        process=Process.sequential,
    )

    # Kickoff the crew
    return crew.kickoff(inputs={"topic": topic, "language": language})
