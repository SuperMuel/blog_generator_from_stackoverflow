from typing import List
from crewai import Task
from textwrap import dedent


class CustomTasks:
    def search_stackoverflow_task(self, agent):
        """Task to search for Stack Overflow posts related to a topic."""
        return Task(
            description=dedent(
                """
                Use the SerperDev tool to search for Stack Overflow posts related to '{topic}'. 
                Select between one and 5 relevant results and obtain the sitelinks for each result.
                The url of an answer is in the format 'https://stackoverflow.com/a/<answer_id>'.
                Even if the topic is in a foreign language, you try to find the best answers from English posts because 
                it's the most common language for programming. You don't need to translate your results.
                For Python topics, don't select answers that you know use python 2 because it's outdated. If you don't know, it's better to select it if the answer seems relevant.
                """
            ),
            expected_output="A list of URLs of the best answers for each selected Stack Overflow post.",
            agent=agent,
        )

    def generate_stackoverflow_technical_report(self, agent):
        """Task to create a detailed technical report from Stack Overflow answers."""
        return Task(
            description=dedent(
                """
                Read the answers from the provided Stack Overflow URLs using the StackOverflowAnswerTool. 
                Create a detailed technical report that focuses on common issues and technical details of the solutions. 
                Ensure that no user-specific references or mentions of Stack Overflow are included. 
                The report should be comprehensive and retain all significant information from the answers.
                It is important to keep what the users struggle with and what they find difficult, so that the blog post can address these issues.
                Include relevant code snippets and explanations in the report.
                """
            ),
            expected_output="A detailed technical report highlighting key problems and solutions from the Stack Overflow answers.",
            agent=agent,
        )

    def find_reliable_sources_task(self, agent):
        """Task to find reliable sources related to a topic for further reading."""
        # TODO : except stackoverflow
        # TODO : instruct to use `site:` syntax to search on specific reliable websites
        # TODO : why does it always make a single search ? Check the instructions. Or maybe instruct to use the | operator to combine multiple searches.
        return Task(
            description=dedent(
                """
                Use the SerperDev tool to search for reliable sources related to '{topic}'.
                NEVER rely on your personal knowledge to provide reliable sources. Always rely on the tools and context provided.
                Focus on finding authoritative and reputable sources such as official documentation.
                You can use multiple web searches using different keywords to find the best sources.
                Avoid sources like SEO-driven blogs or forums unless they are highly reputable.
                You ensure that the sources are well related to the topic. For instance, avoid suggesting React Native sources for a React-only topic.
                It should provide a more in-depth understanding of the topic, but it should not be too advanced for beginners.
                You ensure that the sources are up-to-date. For instance, legacy.reactjs.org/docs/... is not up-to-date but react.dev/reference is.

                When selecting the best sources, explain why you consider them reliable and useful for further reading. 
                For the second and each new source, explain why it is different from the previous one and not redundant. 
                If it is redundant, don't include it in the list and prefer to keep your list small.

                Even if the topic is in a foreign language, you prefer to do web searches with an english query because it's the most common language for programming. You don't need to translate your results.

                Important note : If the tool do not work, or if you can't find any reliable sources, you should answer that you didn't find any reliable sources, or answer with an empty list. Never use your personal knowledge to provide sources.
                """
            ),
            expected_output="A list of reliable sources for further reading. Between 0 and 3 sources.",
            agent=agent,
        )

    def write_task(self, agent, context_tasks: List[Task]):
        """Task to write a detailed blog post based on the previous results."""
        return Task(
            description=dedent(
                """
                Write a comprehensive blog post on "{topic}" based on the summaries of the selected Stack Overflow answers. 
                Ensure the article is informative, engaging, and formatted in markdown. 
                The blog post is targeted towards beginners. 
                Examples are better than theory, so include code snippets and practical examples. 
                Language of the blog post should be {language}.
                Don't try to include any images or diagrams, as we can't generate them.
                Ensure that the article starts with a h1 with the title of the blog post. e.g. "# Title of the blog post"
                Conclude with a 'Further Reading' section, listing only the reliable sources discovered, no invented references.
                Do not explain that the sources are reliable, just list them using the markdown link format.
                Never add additional links that were not given to you.
                """
            ),
            expected_output='A 700 words markdown formatted blog post on "{topic}" in {language}.',
            agent=agent,
            context=context_tasks,
            # TODO Add context, so that it doesn't write "Bienvenue sur ce blog dédié au développement Python ! "
            # TODO : SEO optimization
        )

    def evaluation_task(self, agent, context_tasks: List[Task]):
        """Task to evaluate the blog post generated by the Blog Writer Agent."""
        return Task(
            description=dedent(
                """
                Evaluate the blog post generated by the Blog Writer Agent. Assess the content for readability, accuracy, relevance, and overall quality. 
                Ensure that translations are accurate and coherent, and that code snippets have consistent variable and function names, in the same language (e.g., English or French but not mixed).
                Provide detailed feedback on what could be improved, what might be missing, and any elements that could be removed.
                Verify that the content of the article is closely related and relevant to the assigned topic.
                Ensure that the feedback is constructive and actionable.
                Do not suggest to add diagrams or images, as we can't generate them.
                Do not suggest to change the sources or add new ones, as the sources are already validated. Do not talk about sources. 
                Keep the "Further Reading" section intact as we already know the sources are reliable and useful.
                NEVER suggest to add additional sources.
                Answer in the {language} language. Don't force yourself to use 100% {language} terms if it's not natural. For instance, do not translate "bug" to "bogue" in a French article, but use "bug" instead.
                While your feedback should be written in {language}, you must respect the format of your answer : keep the terms "Thought: " or "Final Answer" in English as requested by the instructions. 
                """  # TODO: Ensure that the code blocks written can run without any errors, or that explanations are provided for any errors that may occur. For instance, imports should be correct, or functions and variables not defined should be explained.
            ),
            # TODO : give the websiteExistsTool to check if the sources are still available.
            expected_output="A detailed feedback report.",
            agent=agent,
            context=context_tasks,
        )  # TODO : sometimes, suggested improvements are pertinent, but would require web searches. We would benefit from an agent that would take the suggestions and decide if web searches are necessary.

    def revision_task(self, agent, context_tasks: List[Task]):
        """Task to revise the blog post based on the evaluation feedback."""
        return Task(
            description=dedent(
                """
                Read the blog post written and the subsequent evaluation feedback. Make necessary revisions based on the feedback provided. 
                Ensure that all suggested improvements are implemented and that the blog post is polished and ready for publication.
                Don't try to include any images or diagrams, as we can't generate them.
                Do not change the sources or add new ones, as the sources are already validated.
                Ensure that the article starts with a h1 with the title of the blog post. e.g. "# Title of the blog post"
                """
            ),
            expected_output='A revised markdown formatted blog post on "{topic}" in {language}.',
            agent=agent,
            context=context_tasks,
        )  # TODO find subjects in the generated blog post that would benefit from a clarification. For instance, if the term "microtask" occurs in a blog on a javascript subject, it should be explained in a way that a beginner can understand, or removed and replaced with simpler terms.

    def link_existing_articles_task(self, agent, existing_articles: List[dict]):
        """Task to add links to existing articles within the new article."""

        assert len(existing_articles) > 0, "At least one existing article is required."
        assert all(
            "title" in article and "url" in article for article in existing_articles
        ), "Each article should have a title and a URL key."

        def format_one_article(article):
            markdown_link = f"[**{article['title']}**]({article['url']})"
            summary = f" - {article['summary']}" if "summary" in article else ""

            return f"- {markdown_link}{summary}"

        articles_list = "\n".join(map(format_one_article, existing_articles))

        return Task(
            description=dedent(
                f"""Review the new article and identify opportunities to add links to existing articles of the blog to enhance its content and provide additional resources for the readers.

            The goal is to add a maximum of 3 highly relevant links within the body of the new article. These links should enhance the content and provide significant additional value to the readers.
            Ensure that the relationship between the new article and the linked articles is clear and contextually relevant. Only add a link if it is highly relevant to the topic being discussed.

            Guidelines for linking:
            - Place the links in areas of the article where they naturally fit and add value to the content.
            - Ensure the links are not inserted in the middle of code snippets or in any way that disrupts the flow of the article.
            - Don't add links to the same article more than once.
            - Don't put multiple links in the same paragraph. Spread them out across the article.
            - Do not assume that the article talks about something if it's not specified in the article summary. It's better to not link than to make an assumption.
            - Each link should be highly relevant to the topic being discussed in the paragraph and should seamlessly integrate into the content.

            If no highly relevant links can be found, just give back the original article without any changes.

            The blog has the following articles that can be linked to:
            <articles_list>

            {articles_list}

            </articles_list>

            Before you proceed, list the articles you plan to link to and their positions in the new article, along with a short explanation of why each link is highly relevant in the context of the new article.

            When you finish, provide the revised article with the added links. If no changes were made, return the original article.
            """
            ),
            agent=agent,
            expected_output="A revised article with highly relevant links to existing articles, or the original article if no highly relevant links were found.",
            # TODO : instruct to introduce the link with a sentence that makes sense in the context of the new article.
            # TODO : it once confused our articles with the reliable sources. Add instructions : "Do not mix up the external sources that are already at the end of the article, with our own articles of {blog_base_url}"
        )
