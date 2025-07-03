from typing import AsyncGenerator, Any, Dict
from datetime import datetime
from openai.agents import AgentResponse

class StreamManager:
    @staticmethod
    async def format_response(response: AgentResponse) -> str:
        if isinstance(response.content, str):
            return response.content
        return str(response.content)

    @staticmethod
    async def stream_with_typing_effect(text: str) -> AsyncGenerator[str, None]:
        words = text.split()
        for i, word in enumerate(words):
            yield word + (" " if i < len(words) - 1 else "")
            await asyncio.sleep(0.1)  # Simulates typing effect

    @staticmethod
    async def format_progress_update(progress: Dict[str, Any]) -> str:
        return f"Progress Update ({datetime.now().strftime('%Y-%m-%d %H:%M')}):" + \
               f"\n- Current Status: {progress.get('status', 'N/A')}" + \
               f"\n- Achievement: {progress.get('achievement', 0)}%" + \
               f"\n- Next Milestone: {progress.get('next_milestone', 'N/A')}"