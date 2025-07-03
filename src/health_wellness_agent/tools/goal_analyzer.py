# Remove openai import
from typing import Dict, Optional
from pydantic import BaseModel
from ..config import GEMINI_API_KEY
import google.generativeai as genai

class GoalAnalyzerTool(Tool):
    def __init__(self):
        super().__init__()
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')

    async def extract_goal_type(self, text: str) -> str:
        prompt = "Extract the type of health/fitness goal from the text."
        response = await self.model.generate_content(f"{prompt}\n\nText: {text}")
        return response.text

    def extract_target_value(self, text: str) -> float:
        prompt = "Extract numerical target value from the text."
        response = self.model.generate_content(f"{prompt}\n\nText: {text}")
        return float(response.text)

    def extract_timeframe(self, text: str) -> int:
        prompt = "Extract timeframe in weeks from the text."
        response = self.model.generate_content(f"{prompt}\n\nText: {text}")
        return int(response.text)

    def validate_goal_safety(self, target: float, timeframe: int) -> None:
        if not self.guardrails.check_progression_rate(0, target, timeframe * 7):
            raise ValueError("Goal progression rate exceeds safe limits")

    def calculate_required_metrics(self, goal_type: str, target: float, current_stats: Dict[str, float]) -> Dict[str, float]:
        metrics = {}
        if goal_type == "weight_loss":
            metrics["daily_calorie_deficit"] = 500
            metrics["weekly_weight_loss"] = 0.5
        elif goal_type == "muscle_gain":
            metrics["daily_calorie_surplus"] = 300
            metrics["weekly_weight_gain"] = 0.25
        return metrics

    def identify_constraints(self, goal_input: GoalInput) -> Dict[str, str]:
        constraints = {}
        if goal_input.current_stats:
            if goal_input.current_stats.get("bmi", 0) > 30:
                constraints["intensity"] = "low_to_moderate"
            if goal_input.current_stats.get("age", 0) > 50:
                constraints["recovery"] = "extended"
        return constraints