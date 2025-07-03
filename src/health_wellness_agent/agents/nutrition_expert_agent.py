from typing import Dict, List, Optional
from pydantic import BaseModel
from openai.agents import Agent, AgentResponse
from ..context import UserSessionContext
from ..config import GEMINI_API_KEY
import google.generativeai as genai

class NutritionExpertAgent(Agent):
    name = "nutrition_expert"
    description = "Specialized agent for handling complex dietary needs and nutrition planning"

    async def handle_nutrition_query(
        self,
        query: str,
        context: UserSessionContext
    ) -> AgentResponse:
        # Analyze nutrition-specific query
        nutrition_analysis = await self.analyze_nutrition_requirements(query, context)
        
        # Generate specialized recommendations
        recommendations = await self.generate_nutrition_recommendations(
            nutrition_analysis,
            context
        )
        
        return AgentResponse(
            content=recommendations,
            context_updates={
                'diet_preferences': nutrition_analysis
            }
        )

    def __init__(self):
        super().__init__()
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')

    async def analyze_nutrition_requirements(self, query: str, context: UserSessionContext) -> Dict:
        prompt = "Analyze dietary requirements and restrictions from the query."
        response = await self.model.generate_content(f"{prompt}\n\nQuery: {query}")
        return self.parse_nutrition_analysis(response.text)
        # Extract dietary restrictions
        restrictions = self.extract_dietary_restrictions(query)
        
        # Identify medical conditions
        medical_conditions = self.identify_medical_conditions(query)
        
        # Calculate nutritional needs
        nutritional_needs = await self.calculate_nutritional_needs(
            context.user_profile,
            medical_conditions
        )
        
        return {
            "restrictions": restrictions,
            "medical_conditions": medical_conditions,
            "nutritional_needs": nutritional_needs
        }

    async def generate_nutrition_recommendations(self, analysis: Dict, context: UserSessionContext) -> str:
        # Generate safe recommendations
        recommendations = await self.create_safe_recommendations(
            analysis,
            context.user_profile
        )
        
        # Add medical disclaimers if needed
        if analysis["medical_conditions"]:
            recommendations += self.add_medical_disclaimers(
                analysis["medical_conditions"]
            )
        
        return recommendations

    async def on_handoff(self, context: UserSessionContext) -> None:
        # Initialize nutrition expert context
        # Log handoff in context
        context.handoff_logs.append(f"Nutrition expert consultation started")