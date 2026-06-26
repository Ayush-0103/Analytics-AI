from tavily import TavilyClient
from dotenv import load_dotenv
import os

load_dotenv()


class ResearchAgent:

    def __init__(self):

        self.client = TavilyClient(
            api_key=os.getenv(
                "TAVILY_API_KEY"
            )
        )

    def research(
        self,
        topic
    ):

        response = self.client.search(
            query=topic,
            max_results=5
        )

        return response