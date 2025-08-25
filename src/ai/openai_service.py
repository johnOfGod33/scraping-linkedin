import os

from dotenv import load_dotenv

from src.models.job_offers import JobOffers

load_dotenv()


class OpenAIService:
    def __init__(self, api_key: str):
        self.api_key = os.getenv("OPENAI_API_KEY")

    def extract_job_offers(self, html: str) -> JobOffers:
        pass
