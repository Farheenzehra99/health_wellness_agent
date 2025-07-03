from typing import List, Dict, Optional
from datetime import datetime
from pydantic import BaseModel
from openai.agents import Tool

class ProgressMetrics(BaseModel):
    date: datetime
    weight: Optional[float] = None
    measurements: Optional[Dict[str, float]] = None
    energy_levels: Optional[int] = None
    workout_compliance: Optional[float] = None
    diet_compliance: Optional[float] = None
    notes: Optional[str] = None

class ProgressAnalysis(BaseModel):
    metrics_history: List[ProgressMetrics]
    trend_analysis: Dict[str, float]
    goal_progress: Dict[str, float]
    recommendations: Dict[str, str]

class ProgressTrackerTool(Tool):
    name = "progress_tracker"
    description = "Tracks and analyzes user progress towards health and fitness goals"

    async def run(
        self,
        new_metrics: ProgressMetrics,
        goal_output: GoalOutput,
        history: List[ProgressMetrics]
    ) -> ProgressAnalysis:
        # Update metrics history
        updated_history = self.update_history(history, new_metrics)
        
        # Analyze trends
        trends = self.analyze_trends(updated_history)
        
        # Calculate progress towards goals
        progress = self.calculate_goal_progress(updated_history, goal_output)
        
        # Generate recommendations
        recommendations = await self.generate_recommendations(
            progress,
            trends,
            goal_output
        )
        
        return ProgressAnalysis(
            metrics_history=updated_history,
            trend_analysis=trends,
            goal_progress=progress,
            recommendations=recommendations
        )

    def update_history(self, history: List[ProgressMetrics], new_metrics: ProgressMetrics) -> List[ProgressMetrics]:
        # Validate new metrics
        self.validate_metrics(new_metrics)
        
        # Add to history
        updated_history = history.copy()
        updated_history.append(new_metrics)
        
        # Sort by date
        return sorted(updated_history, key=lambda x: x.date)

    def analyze_trends(self, history: List[ProgressMetrics]) -> Dict[str, float]:
        # Calculate rate of change for each metric
        trends = {}
        for metric in ["weight", "energy_levels", "workout_compliance", "diet_compliance"]:
            trends[f"{metric}_trend"] = self.calculate_trend(history, metric)
        return trends

    def calculate_goal_progress(self, history: List[ProgressMetrics], goal_output: GoalOutput) -> Dict[str, float]:
        # Calculate progress percentage
        initial = history[0]
        current = history[-1]
        target = goal_output.target_value
        
        progress = {
            "overall_progress": self.calculate_overall_progress(initial, current, target),
            "weekly_progress": self.calculate_weekly_progress(history),
            "projected_completion": self.project_completion_time(history, target)
        }
        return progress

    async def generate_recommendations(self, progress: Dict[str, float], trends: Dict[str, float], goal_output: GoalOutput) -> Dict[str, str]:
        # Analyze progress and trends
        recommendations = {}
        
        # Generate diet recommendations
        if self.needs_diet_adjustment(progress, trends):
            recommendations["diet"] = await self.get_diet_recommendations(progress)
        
        # Generate workout recommendations
        if self.needs_workout_adjustment(progress, trends):
            recommendations["workout"] = await self.get_workout_recommendations(progress)
        
        return recommendations