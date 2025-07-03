from typing import List, Dict, Optional
from pydantic import BaseModel
from openai.agents import Tool
from ..config import GEMINI_API_KEY
import google.generativeai as genai

class FitnessLevel(BaseModel):
    experience: str  # "beginner", "intermediate", "advanced"
    current_activity: str
    limitations: List[str] = []

class WorkoutPlan(BaseModel):
    weekly_schedule: Dict[str, Dict[str, str]]
    exercises: List[Dict[str, str]]
    progression_plan: Dict[str, str]

class WorkoutRecommenderTool(Tool):
    name = "workout_recommender"
    description = "Generates personalized workout plans based on user goals and fitness level"

    async def run(self, goal_output: GoalOutput, fitness_level: FitnessLevel) -> WorkoutPlan:
        # Generate base workout schedule
        schedule = self.create_weekly_schedule(fitness_level)
        
        # Select appropriate exercises
        exercises = self.select_exercises(
            goal_output,
            fitness_level,
            schedule
        )
        
        # Create progression plan
        progression = self.create_progression_plan(
            exercises,
            goal_output.timeframe_weeks
        )
        
        return WorkoutPlan(
            weekly_schedule=schedule,
            exercises=exercises,
            progression_plan=progression
        )

    def create_weekly_schedule(self, fitness_level: FitnessLevel) -> Dict[str, Dict[str, str]]:
        # Create schedule based on experience level
        if fitness_level.experience == "beginner":
            return self.create_beginner_schedule()
        elif fitness_level.experience == "intermediate":
            return self.create_intermediate_schedule()
        else:
            return self.create_advanced_schedule()

    def __init__(self):
        super().__init__()
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')

    async def select_exercises(self, goal_output: GoalOutput, fitness_level: FitnessLevel, schedule: Dict[str, Dict[str, str]]) -> List[Dict[str, str]]:
        prompt = self.create_exercise_prompt(goal_output, fitness_level, schedule)
        response = await self.model.generate_content(prompt)
        return self.parse_exercise_recommendations(response.text)

    def create_progression_plan(self, exercises: List[Dict[str, str]], timeframe: int) -> Dict[str, str]:
        # Create progressive overload plan
        progression = {}
        for exercise in exercises:
            progression[exercise["name"]] = self.plan_exercise_progression(
                exercise,
                timeframe
            )
        return progression