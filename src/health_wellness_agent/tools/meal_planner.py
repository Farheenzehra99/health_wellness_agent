from typing import List, Dict, Optional
from pydantic import BaseModel
from openai.agents import Tool

class DietaryPreferences(BaseModel):
    restrictions: List[str] = []
    allergies: List[str] = []
    preferred_cuisine: List[str] = []
    calories_target: Optional[int] = None

class Meal(BaseModel):
    name: str
    ingredients: List[str]
    nutrition: Dict[str, float]
    preparation: str
    portion_size: str

class DailyPlan(BaseModel):
    breakfast: Meal
    lunch: Meal
    dinner: Meal
    snacks: List[Meal]
    total_nutrition: Dict[str, float]

class MealPlan(BaseModel):
    daily_plans: Dict[str, DailyPlan]
    shopping_list: List[str]
    nutritional_summary: Dict[str, float]

class MealPlannerTool(Tool):
    name = "meal_planner"
    description = "Generates personalized meal plans based on user goals and preferences"

    async def run(
        self,
        goal_output: GoalOutput,
        preferences: DietaryPreferences
    ) -> MealPlan:
        # Calculate daily nutritional needs
        nutrition_targets = self.calculate_nutrition_targets(goal_output)
        
        # Generate weekly meal plan
        daily_plans = await self.generate_daily_plans(
            nutrition_targets,
            preferences
        )
        
        # Create shopping list
        shopping_list = self.create_shopping_list(daily_plans)
        
        # Calculate nutritional summary
        nutritional_summary = self.calculate_nutritional_summary(daily_plans)
        
        return MealPlan(
            daily_plans=daily_plans,
            shopping_list=shopping_list,
            nutritional_summary=nutritional_summary
        )

    def calculate_nutrition_targets(self, goal_output: GoalOutput) -> Dict[str, float]:
        # Calculate daily caloric needs
        base_calories = self.calculate_base_calories(goal_output)
        
        # Adjust for goal type
        adjusted_calories = self.adjust_calories_for_goal(base_calories, goal_output)
        
        # Calculate macronutrient ratios
        macros = self.calculate_macronutrient_split(adjusted_calories, goal_output)
        
        # Add micronutrient targets
        micros = self.calculate_micronutrient_needs(goal_output)
        
        return {
            "calories": adjusted_calories,
            **macros,
            **micros
        }

    async def generate_daily_plans(self, targets: Dict[str, float], preferences: DietaryPreferences) -> Dict[str, DailyPlan]:
        # Generate meal combinations
        daily_plans = {}
        for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
            meals = await self.generate_meals_for_day(targets, preferences)
            daily_plans[day] = DailyPlan(**meals)
        return daily_plans

    def create_shopping_list(self, daily_plans: Dict[str, DailyPlan]) -> List[str]:
        # Extract all ingredients
        all_ingredients = set()
        for plan in daily_plans.values():
            for meal in [plan.breakfast, plan.lunch, plan.dinner] + plan.snacks:
                all_ingredients.update(meal.ingredients)
        
        # Organize by category
        return sorted(list(all_ingredients))

    def calculate_nutritional_summary(self, daily_plans: Dict[str, DailyPlan]) -> Dict[str, float]:
        # Calculate weekly totals
        weekly_totals = {}
        for plan in daily_plans.values():
            for nutrient, value in plan.total_nutrition.items():
                weekly_totals[nutrient] = weekly_totals.get(nutrient, 0) + value
        
        # Calculate averages
        return {k: v/7 for k, v in weekly_totals.items()}