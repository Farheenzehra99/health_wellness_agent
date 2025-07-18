from typing import AsyncGenerator, Any, Dict
from datetime import datetime

class StreamingManager:
    @staticmethod
    async def create_progress_stream(total_steps: int) -> AsyncGenerator[Dict[str, Any], None]:
        start_time = datetime.now()
        
        for step in range(total_steps):
            progress = (step + 1) / total_steps * 100
            elapsed = (datetime.now() - start_time).seconds
            
            yield {
                "step": step + 1,
                "total_steps": total_steps,
                "progress_percentage": progress,
                "elapsed_seconds": elapsed,
                "estimated_remaining": int(elapsed * (100 - progress) / progress) if progress > 0 else None
            }
            
            await asyncio.sleep(0.1)  # Prevent flooding

class StreamingResponse(BaseModel):
    progress: Dict[str, Any]
    partial_result: Optional[Any] = None
    is_complete: bool = False
    error: Optional[str] = None