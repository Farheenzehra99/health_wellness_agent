from typing import List, Dict, Optional
from pydantic import BaseModel
from openai.agents import Tool, StreamingResponse

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

from typing import List, Dict, Optional, AsyncGenerator
from pydantic import BaseModel
from openai.agents import Tool, StreamingResponse

class MealPlannerTool(AsyncToolBase):
    name = "meal_planner"
    description = "Generates personalized meal plans based on user goals and preferences"

    async def validate_input(self, goal_output: GoalOutput, preferences: DietaryPreferences) -> bool:
        if not goal_output or not preferences:
            return False
        if not preferences.calories_target:
            return False
        return True

    async def execute(self, goal_output: GoalOutput, preferences: DietaryPreferences) -> StreamingResponse[MealPlan]:
        nutrition_targets = self.calculate_nutrition_targets(goal_output)
        
        return StreamingResponse(
            final_response=MealPlan(
                daily_plans=await self.generate_daily_plans(nutrition_targets, preferences),
                shopping_list=self.create_shopping_list(daily_plans),
                nutritional_summary=self.calculate_nutritional_summary(daily_plans)
            ),
            progress_generator=self.generate_meal_stream(nutrition_targets, preferences)
        )

    async def post_execute(self, result: StreamingResponse[MealPlan]) -> StreamingResponse[MealPlan]:
        # Add any post-processing logic here
        return result

    async def generate_meal_stream(self, nutrition_targets: Dict[str, float], preferences: DietaryPreferences) -> AsyncGenerator[str, None]:
        total_steps = 7  # days in week
        for day_num in range(total_steps):
            day = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"][day_num]
            yield f"Generating meal plan for {day}..."
            
            meals = await self.generate_meals_for_day(nutrition_targets, preferences)
            yield f"Completed {day}'s meal plan: {meals['breakfast'].name}, {meals['lunch'].name}, {meals['dinner'].name}"

    async def run(
        self,
        goal_output: GoalOutput,
        preferences: DietaryPreferences
    ) -> StreamingResponse[MealPlan]:
        nutrition_targets = self.calculate_nutrition_targets(goal_output)
        
        return StreamingResponse(
            final_response=MealPlan(
                daily_plans=await self.generate_daily_plans(nutrition_targets, preferences),
                shopping_list=self.create_shopping_list(daily_plans),
                nutritional_summary=self.calculate_nutritional_summary(daily_plans)
            ),
            progress_generator=self.generate_meal_stream(nutrition_targets, preferences)
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

    async def generate_meal_plan(self, preferences: Dict) -> AsyncGenerator[str, None]:
        # Initial response
        yield "Analyzing your dietary preferences..."
        await asyncio.sleep(0.5)
        
        # Generate meal plan day by day
        for day in range(1, 8):
            yield f"\nGenerating meal plan for Day {day}..."
            await asyncio.sleep(0.5)
            # Generate meals for the day
            yield f"Breakfast: {await self.generate_meal('breakfast', preferences)}"
            yield f"Lunch: {await self.generate_meal('lunch', preferences)}"
            yield f"Dinner: {await self.generate_meal('dinner', preferences)}"

    async def __call__(self, **kwargs) -> StreamingResponse:
        return StreamingResponse(self.generate_meal_plan(kwargs))