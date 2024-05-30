from crewai import Task
from textwrap import dedent


class CustomTasks:
    def search_task(self, agent):
        return Task(
            description=dedent(
                """
                Use the SerperDev tool to search for Stack Overflow posts related to '{topic}'. 
                Select between one and three relevant results and obtain the sitelinks for each result.
                The url of an answer is in the format 'https://stackoverflow.com/a/<answer_id>'.
                Even if the topic is in a foreign language, you try to find the best answers from English posts because 
                it's the most common language for programming. You don't need to translate your results.
                """
            ),
            expected_output="A list of URLs of the best answers for each selected Stack Overflow post.",
            agent=agent,
        )

    def report_task(self, agent):
        return Task(
            description=dedent(
                """
                Read the answers from the provided Stack Overflow URLs using the StackOverflowAnswerTool. 
                Create a detailed technical report that focuses on common issues and technical details of the solutions. 
                Ensure that no user-specific references or mentions of Stack Overflow are included. 
                The report should be comprehensive and retain all significant information from the answers.
                Include relevant code snippets and explanations in the report.
                """
            ),
            expected_output="A detailed technical report highlighting key problems and solutions from the Stack Overflow answers.",
            agent=agent,
        )

    def write_task(self, agent, topic, language):
        return Task(
            description=dedent(
                f"""
                Write a comprehensive blog post on {topic} based on the summaries of the selected Stack Overflow answers. 
                Ensure the article is informative, engaging, and formatted in markdown. 
                The blog post is targeted towards beginners. 
                Examples are better than theory, so include code snippets and practical examples. 
                Language of the blog post should be {language}.
                Don't try to include any images or diagrams, as we can't generate them.
                Do not include sources or references, as this task will be handled separately.
                """
            ),
            expected_output=f"A markdown formatted blog post on {topic} in {language}.",
            agent=agent,
        )

    def evaluation_task(self, agent, context_task):
        return Task(
            description=dedent(
                """
                Evaluate the blog post generated by the Blog Writer Agent. Assess the content for readability, accuracy, relevance, and overall quality. 
                Ensure that translations are accurate and coherent, and that code snippets have consistent variable and function names, in the same language (e.g., English or French but not mixed).
                Provide detailed feedback on what could be improved, what might be missing, and any elements that could be removed.
                Verify that the content of the article is closely related and relevant to the assigned topic.
                Ensure that the feedback is constructive and actionable.
                Don't suggest to add diagrams or images, as we can't generate them. 
                Don't suggest to add references, as this task will be handled separately.
                """
            ),
            expected_output="A detailed feedback report.",
            agent=agent,
            context=[context_task],
        )

    def revision_task(self, agent, context_tasks, topic, language):
        return Task(
            description=dedent(
                """
                Read the blog post written and the subsequent evaluation feedback. Make necessary revisions based on the feedback provided. 
                Ensure that all suggested improvements are implemented and that the blog post is polished and ready for publication.
                Don't try to include any images or diagrams, as we can't generate them.
                Do not include sources or references, as this task will be handled separately.
                """
            ),
            expected_output=f"A revised markdown formatted blog post on {topic} in {language}.",
            agent=agent,
            context=context_tasks,
        )
