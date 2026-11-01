from config.settings import get_gemini_credentials
from gemini_webapi import GeminiClient


class GeminiWebClient:

    def __init__(self):
        self.psid, self.psidts = get_gemini_credentials()
        self.client = None

    async def init_client(self):
        if not self.client:
            self.client = GeminiClient(
                self.psid, self.psidts if self.psidts else None
            )
            await self.client.init(
                timeout=30, auto_close=False, close_delay=300
            )

    async def ask(self, prompt: str) -> str:
        await self.init_client()
        response = await self.client.generate_content(prompt)
        return response.text
