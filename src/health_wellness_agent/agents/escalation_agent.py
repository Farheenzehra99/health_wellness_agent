from typing import Dict, Optional
from pydantic import BaseModel
from openai.agents import Agent, AgentResponse
from ..context import UserSessionContext

class EscalationAgent(Agent):
    name = "escalation"
    description = "Handles escalation to human coaches and manages handoff process"

    async def handle_escalation(self, query: str, context: UserSessionContext) -> AgentResponse:
        # Analyze escalation reason
        escalation_details = await self.analyze_escalation_need(query, context)
        
        # Log handoff in context
        context.handoff_logs.append({
            "timestamp": datetime.now(),
            "from_agent": "main",
            "to_agent": "escalation",
            "reason": escalation_details["triggers"],
            "urgency": escalation_details["urgency"]
        })
        
        # Prepare handoff summary
        coach_summary = self.prepare_coach_summary(context, escalation_details)
        
        # Generate interim guidance
        interim_guidance = await self.provide_interim_guidance(escalation_details)
        
        # Update context with escalation status
        context.escalation_status = {
            "status": "pending_coach_review",
            "timestamp": datetime.now(),
            "details": escalation_details
        }
        
        return AgentResponse(
            content={
                'coach_summary': coach_summary,
                'interim_guidance': interim_guidance
            },
            context_updates={
                'escalation_status': context.escalation_status,
                'handoff_logs': context.handoff_logs
            }
        )

    async def analyze_escalation_need(self, query: str, context: UserSessionContext) -> Dict:
        # Identify escalation triggers
        triggers = self.identify_escalation_triggers(query)
        
        # Assess urgency
        urgency = self.assess_urgency(triggers)
        
        # Determine required expertise
        expertise = self.determine_required_expertise(triggers)
        
        return {
            "triggers": triggers,
            "urgency": urgency,
            "required_expertise": expertise,
            "user_history": self.get_relevant_history(context)
        }

    def prepare_coach_summary(self, context: UserSessionContext, details: Dict) -> Dict:
        return {
            "user_profile": context.user_profile,
            "current_goals": context.goals,
            "progress_history": context.progress_history,
            "escalation_reason": details["triggers"],
            "urgency_level": details["urgency"],
            "required_expertise": details["required_expertise"]
        }

    def provide_interim_guidance(self, details: Dict) -> str:
        # Generate safe temporary guidance
        guidance = self.generate_safe_guidance(details["triggers"])
        
        # Add urgency-specific instructions
        if details["urgency"] == "high":
            guidance += self.add_urgent_care_instructions()
        
        # Add expertise-specific waiting instructions
        guidance += self.add_expertise_waiting_instructions(
            details["required_expertise"]
        )
        
        return guidance

    async def on_handoff(self, context: UserSessionContext) -> None:
        # Log escalation request
        context.handoff_logs.append(f"Escalation to human coach initiated")