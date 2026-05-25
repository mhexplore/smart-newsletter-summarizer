"""
CrewAI crew: News Scout → Fact Checker → Newsletter Editor.
Uses GPT-4o-mini via OPENAI_API_KEY.
"""

import os
from pathlib import Path

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from src.config.env import load_app_env, require_env_vars
from src.tools.crew_tools import (
    rss_feed_reader,
    tavily_news_search,
    verify_all_urls_in_text,
    verify_single_url,
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = PROJECT_ROOT / "output"


@CrewBase
class NewsletterCrew:
    """Smart Newsletter Summarizer crew."""

    agents_config = str(PROJECT_ROOT / "config" / "agents.yaml")
    tasks_config = str(PROJECT_ROOT / "config" / "tasks.yaml")

    @agent
    def news_scout(self) -> Agent:
        return Agent(
            config=self.agents_config["news_scout"],  # type: ignore[index]
            tools=[rss_feed_reader, tavily_news_search],
            llm="gpt-4o-mini",
            verbose=True,
            allow_delegation=False,
        )

    @agent
    def fact_checker(self) -> Agent:
        return Agent(
            config=self.agents_config["fact_checker"],  # type: ignore[index]
            tools=[
                verify_single_url,
                verify_all_urls_in_text,
                tavily_news_search,
            ],
            llm="gpt-4o-mini",
            verbose=True,
            allow_delegation=False,
        )

    @agent
    def summarizer(self) -> Agent:
        return Agent(
            config=self.agents_config["summarizer"],  # type: ignore[index]
            llm="gpt-4o-mini",
            verbose=True,
            allow_delegation=False,
        )

    @task
    def scout_task(self) -> Task:
        return Task(
            config=self.tasks_config["scout_task"],  # type: ignore[index]
            agent=self.news_scout(),
            output_file=str(OUTPUT_DIR / "scout_report.md"),
        )

    @task
    def fact_check_task(self) -> Task:
        return Task(
            config=self.tasks_config["fact_check_task"],  # type: ignore[index]
            agent=self.fact_checker(),
            context=[self.scout_task()],
            output_file=str(OUTPUT_DIR / "fact_check_report.md"),
        )

    @task
    def summarize_task(self) -> Task:
        return Task(
            config=self.tasks_config["summarize_task"],  # type: ignore[index]
            agent=self.summarizer(),
            context=[self.fact_check_task()],
            output_file=str(OUTPUT_DIR / "newsletter.md"),
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )


def run_newsletter_crew(topic: str) -> str:
    """
    Run Scout → Fact Checker → Editor for a topic or RSS feed URL.

    Args:
        topic: Search keywords OR a full RSS feed URL.

    Returns:
        Final newsletter Markdown string.
    """
    load_app_env(PROJECT_ROOT)
    require_env_vars("OPENAI_API_KEY", context="NewsletterCrew / OpenAI")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    os.chdir(PROJECT_ROOT)
    os.environ["NEWSLETTER_TOPIC"] = topic
    result = NewsletterCrew().crew().kickoff(inputs={"topic": topic})
    return str(result)
