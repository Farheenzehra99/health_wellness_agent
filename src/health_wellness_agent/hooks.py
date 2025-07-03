from typing import Any, Dict, Optional
from datetime import datetime
from openai.agents import RunHooks, AgentHooks
from .context import UserSessionContext

class HealthWellnessRunHooks(RunHooks):
    async def on_agent_start(self, agent_name: str, context: UserSessionContext) -> None:
        context.update_last_interaction()
        print(f"Agent {agent_name} started at {datetime.now()}")

    async def on_agent_end(self, agent_name: str, context: UserSessionContext) -> None:
        duration = datetime.now() - context.last_interaction
        print(f"Agent {agent_name} completed in {duration.seconds} seconds")

    async def on_tool_start(self, tool_name: str, context: UserSessionContext) -> None:
        print(f"Tool {tool_name} started at {datetime.now()}")

    async def on_tool_end(self, tool_name: str, context: UserSessionContext) -> None:
        print(f"Tool {tool_name} completed at {datetime.now()}")

    async def on_handoff(self, from_agent: str, to_agent: str, context: UserSessionContext) -> None:
        context.log_handoff(to_agent, f"Handoff from {from_agent}")

class HealthWellnessAgentHooks(AgentHooks):
    async def on_start(self, context: UserSessionContext) -> None:
        # Initialize agent-specific metrics
        context.session_metrics['tool_calls'] = 0
        context.session_metrics['handoffs'] = 0

    async def on_end(self, context: UserSessionContext) -> None:
        # Log session summary
        print(f"Session completed with {context.session_metrics['tool_calls']} tool calls")

    async def on_tool_start(self, tool_name: str, context: UserSessionContext) -> None:
        context.session_metrics['tool_calls'] += 1

    async def on_handoff(self, to_agent: str, context: UserSessionContext) -> None:
        context.session_metrics['handoffs'] += 1