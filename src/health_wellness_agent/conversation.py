from typing import Dict, List, Optional
from pydantic import BaseModel

class ConversationState(BaseModel):
    current_topic: str
    missing_info: List[str] = []
    context: Dict[str, any] = {}
    follow_up_questions: List[str] = []

class ConversationManager:
    def __init__(self):
        self.state = ConversationState(current_topic="initial")
        self.required_fields = {
            "goal_setting": ["target", "timeframe", "current_status"],
            "diet_planning": ["dietary_restrictions", "allergies", "preferences"],
            "workout_planning": ["fitness_level", "equipment_access", "time_availability"]
        }

    def analyze_input(self, user_input: str) -> Dict[str, any]:
        # Identify topic and extract information
        topic = self.identify_topic(user_input)
        extracted_info = self.extract_information(user_input)
        
        # Update conversation state
        self.state.current_topic = topic
        self.state.context.update(extracted_info)
        
        # Check for missing information
        self.state.missing_info = self.identify_missing_info(topic)
        
        # Generate follow-up questions
        self.state.follow_up_questions = self.generate_follow_up_questions()
        
        return {
            "topic": topic,
            "extracted_info": extracted_info,
            "missing_info": self.state.missing_info,
            "follow_up_questions": self.state.follow_up_questions
        }

    def identify_missing_info(self, topic: str) -> List[str]:
        required = self.required_fields.get(topic, [])
        return [field for field in required if field not in self.state.context]

    def generate_follow_up_questions(self) -> List[str]:
        questions = []
        for missing in self.state.missing_info:
            question = self.create_question_for_field(missing)
            questions.append(question)
        return questions

    def create_question_for_field(self, field: str) -> str:
        questions_map = {
            "target": "What specific goal would you like to achieve?",
            "timeframe": "In how much time would you like to achieve this goal?",
            "dietary_restrictions": "Do you have any dietary restrictions I should know about?",
            # Add more question mappings
        }
        return questions_map.get(field, f"Could you please provide information about your {field}?")