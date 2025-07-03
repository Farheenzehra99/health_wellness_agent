from typing import Any, Dict, Optional
from pydantic import BaseModel, validator
from datetime import datetime, timedelta

class InputGuardrails(BaseModel):
    SAFE_WEIGHT_CHANGE_RATE = 1.0  # kg per week
    MIN_CALORIES = 1200
    MAX_CALORIES = 4000
    MIN_AGE = 18
    MAX_AGE = 100
    MAX_WORKOUT_DURATION = 120  # minutes
    MIN_REST_BETWEEN_SETS = 30  # seconds
    MAX_HEART_RATE = 220  # minus age

    @validator('goal_text')
    def validate_goal_text(cls, v: str) -> str:
        if len(v.split()) < 3:
            raise ValueError("Goal description too short. Please provide more details.")
        if any(word.lower() in v.lower() for word in ['immediate', 'fast', 'quick', 'rapid']):
            raise ValueError("Goals promoting rapid changes are not allowed")
        return v

    @validator('exercise_intensity')
    def validate_intensity(cls, v: float, values: Dict[str, Any]) -> float:
        age = values.get('age', 30)
        max_heart_rate = cls.MAX_HEART_RATE - age
        if v > 0.85 * max_heart_rate:
            raise ValueError("Exercise intensity too high for age")
        return v

class SafetyChecks:
    @staticmethod
    def check_medical_safety(context: Dict) -> bool:
        medical_conditions = context.get('medical_conditions', [])
        high_risk_conditions = [
            'heart_disease', 
            'uncontrolled_diabetes',
            'severe_hypertension',
            'recent_surgery',
            'acute_injury'
        ]
        if any(cond in medical_conditions for cond in high_risk_conditions):
            raise ValueError("Medical clearance required before proceeding")
        return True

    @staticmethod
    def validate_workout_progression(old_plan: Dict, new_plan: Dict) -> bool:
        # Check intensity increase
        old_intensity = old_plan.get('intensity', 0)
        new_intensity = new_plan.get('intensity', 0)
        if new_intensity > old_intensity * 1.1:  # max 10% increase
            raise ValueError("Intensity increase too aggressive")
        return True

    @staticmethod
    def check_progression_rate(old_value: float, new_value: float, timeframe_days: int) -> bool:
        change_rate = abs(new_value - old_value) / timeframe_days * 7  # per week
        return change_rate <= InputGuardrails.SAFE_WEIGHT_CHANGE_RATE