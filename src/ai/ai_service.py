import os

from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.deepseek import DeepSeekProvider
from pydantic_ai.providers.ollama import OllamaProvider
from pydantic_ai.providers.openai import OpenAIProvider

from models.job_offers import JobOffers

load_dotenv()


class AIService:
    def __init__(self, deepseek_api_key: str = None, openai_api_key: str = None):
        self.model = self._get_model(deepseek_api_key, openai_api_key)

    def _get_model(self, deepseek_api_key: str = None, openai_api_key: str = None):
        if openai_api_key:
            return OpenAIModel(
                "gpt-4o",
                provider=OpenAIProvider(
                    api_key=openai_api_key or os.getenv("OPENAI_API_KEY")
                ),
            )
        elif deepseek_api_key:
            return OpenAIModel(
                "deepseek-chat",
                provider=DeepSeekProvider(
                    api_key=deepseek_api_key or os.getenv("DEEPSEEK_API_KEY")
                ),
            )
        else:
            # return ollama local model
            print("Using local Ollama model")
            return OpenAIModel(
                model_name="llama3.2",
                provider=OllamaProvider(base_url="http://localhost:11434/v1"),
            )

    async def test_model(self, prompt: str) -> str:
        agent = Agent(
            model=self.model,
            system_prompt="You are a helpful assistant.",
            output_type=str,
        )

        response = await agent.run(prompt)

        return response.output

    async def extract_job_offers(self, html: str) -> JobOffers:
        system_prompt = """
            You are a specialized HTML parser designed to extract job offer information from HTML content. Your task is to analyze the provided HTML and extract structured job data according to a specific schema.
            **Output Requirements:**
            - Return the extracted data as a valid JSON object
            - Follow the exact field names and types specified in the schema
            - If a field cannot be found or determined from the HTML, use `null` for optional fields or reasonable defaults
            - Ensure date formats are ISO 8601 compliant (YYYY-MM-DDTHH:MM:SS)
            - Work model must be one of: "Full-time", "Part-time", "Freelance", or "Hybrid"

            **Extraction Guidelines:**
            - Look for job titles in heading tags (h1, h2, h3) or elements with classes/ids containing "title", "job", "position"
            - Search for descriptions in div elements, paragraph tags, or sections with classes like "description", "details", "summary"
            - Company information may be in separate sections or embedded within the job posting
            - Posted dates often appear near timestamps, "posted", "published" text, or in meta elements
            - Applicant counts might be shown as numbers followed by "applicants", "applications", or similar terms
            - Work models can be inferred from text mentioning remote, on-site, hybrid, full-time, part-time, contract, or freelance

            **Schema Reference:**
            {
            "title": "string",
            "description": "string", 
            "company_details": {}, 
            "post_at": "datetime (ISO 8601)",
            "applicants": "integer",
            "work_model": "Full-time|Part-time|Freelance|Hybrid"
            }

            Be thorough but accurate. If information is ambiguous, make reasonable inferences based on context clues.
        """

        user_prompt = f"""
        Extract job offer information from the following HTML content and return it as a JSON object matching the specified schema:

        **HTML Content:**
        {html}

        Please analyze the HTML carefully and extract all available information. If certain fields cannot be determined from the HTML content, use appropriate null values or reasonable defaults.
        """

        agent = Agent(
            model=self.model,
            system_prompt=system_prompt,
            output_type=JobOffers,
        )

        response = await agent.run(user_prompt)

        return response.output
