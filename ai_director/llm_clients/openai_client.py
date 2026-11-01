import os


class OpenAIFallbackClient:

    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY", "")

    async def ask(self, prompt: str) -> str:
        raise NotImplementedError(
            "Gemini Web API with cookies is the primary configured provider."
)
