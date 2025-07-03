from typing import Optional
from datetime import datetime
from openai.agents import Runner
from .agent import HealthWellnessAgent
from .context import UserSessionContext, UserProfile
from .hooks import HealthWellnessRunHooks, HealthWellnessAgentHooks

async def initialize_session(user_id: str) -> UserSessionContext:
    # Create initial user profile and context
    profile = UserProfile(
        user_id=user_id,
        name="",
        age=0,
        gender="",
        height=0.0,
        weight=0.0
    )
    
    return UserSessionContext(profile=profile)

async def process_user_input(
    user_input: str,
    context: Optional[UserSessionContext] = None,
    user_id: Optional[str] = None
) -> UserSessionContext:
    # Initialize or use existing context
    if context is None:
        if user_id is None:
            raise ValueError("Either context or user_id must be provided")
        context = await initialize_session(user_id)

    # Create agent and hooks
    agent = HealthWellnessAgent()
    run_hooks = HealthWellnessRunHooks()
    agent_hooks = HealthWellnessAgentHooks()

    # Process input with streaming
    async for step in Runner.stream(
        starting_agent=agent,
        input=user_input,
        context=context,
        run_hooks=run_hooks,
        agent_hooks=agent_hooks
    ):
        # Stream response to user
        print(step.pretty_output)

    return context

def main():
    import asyncio
    
    async def run_session():
        context = None
        while True:
            user_input = input("You: ")
            if user_input.lower() in ['exit', 'quit']:
                break
                
            context = await process_user_input(
                user_input,
                context=context,
                user_id="test_user"
            )

    asyncio.run(run_session())

if __name__ == "__main__":
    main()