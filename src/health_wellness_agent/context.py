from dataclasses import dataclass
from typing import Optional

@dataclass
class UserSessionContext:
    name: str
    uid: int
    age: Optional[int] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    bmi: Optional[float] = None
    goals: List[Dict[str, Any]] = field(default_factory=list)
    progress_history: List[Dict[str, Any]] = field(default_factory=list)
    medical_conditions: List[str] = field(default_factory=list)
    dietary_preferences: List[str] = field(default_factory=list)
    fitness_level: Optional[str] = None
    handoff_logs: List[str] = field(default_factory=list)
    last_checkin: Optional[datetime] = None
    current_streak: int = 0
    achievements: List[str] = field(default_factory=list)


class ConversationManager:
    def __init__(self):
        self.conversation_state = {}
        self.current_flow = None
        self.required_info = set()

    async def manage_conversation(self, message: str, context: UserSessionContext) -> str:
        # Update conversation state
        self.update_state(message, context)

        # Check if we need more information
        if missing_info := self.check_required_info():
            return self.generate_follow_up_question(missing_info)

        # Process complete information
        return await self.process_complete_flow(context)

    def update_state(self, message: str, context: UserSessionContext) -> None:
        # Extract information from message
        extracted_info = self.extract_info(message)
        self.conversation_state.update(extracted_info)

        # Update required information based on flow
        self.update_required_info()