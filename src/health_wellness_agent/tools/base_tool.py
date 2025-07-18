from typing import Any, Dict, Optional
from abc import ABC, abstractmethod
from pydantic import BaseModel
from openai.agents import Tool

class AsyncToolBase(Tool, ABC):
    max_retries: int = 3
    retry_delay: float = 1.0

    @abstractmethod
    async def execute(self, **kwargs) -> Any:
        """Main execution logic for the tool"""
        pass

    @abstractmethod
    async def validate_input(self, **kwargs) -> bool:
        """Validate input parameters"""
        pass

    async def pre_execute(self, **kwargs) -> Dict[str, Any]:
        """Pre-execution setup and validation"""
        if not await self.validate_input(**kwargs):
            raise ValueError("Invalid input parameters")
        return kwargs

    async def post_execute(self, result: Any) -> Any:
        """Post-execution processing"""
        return result

    async def run(self, **kwargs) -> Any:
        retry_count = 0
        last_error = None

        while retry_count < self.max_retries:
            try:
                # Pre-execution setup
                validated_params = await self.pre_execute(**kwargs)
                
                # Main execution
                result = await self.execute(**validated_params)
                
                # Post-execution processing
                return await self.post_execute(result)
                
            except Exception as e:
                last_error = e
                retry_count += 1
                if retry_count < self.max_retries:
                    await asyncio.sleep(self.retry_delay * retry_count)
                continue

        raise Exception(f"Tool execution failed after {self.max_retries} retries. Last error: {str(last_error)}")