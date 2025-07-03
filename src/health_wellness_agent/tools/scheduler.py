from typing import List, Dict, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel
from openai.agents import Tool

class CheckinSchedule(BaseModel):
    frequency: str
    preferred_time: str
    timezone: str
    reminder_method: str

class ScheduledCheckin(BaseModel):
    datetime: datetime
    checkin_type: str
    metrics_required: List[str]
    questions: List[str]

class CheckinSchedulerTool(Tool):
    name = "checkin_scheduler"
    description = "Schedules and manages regular progress check-ins"

    async def run(
        self,
        schedule_preferences: CheckinSchedule,
        goal_output: GoalOutput
    ) -> List[ScheduledCheckin]:
        # Generate checkin schedule
        checkins = self.generate_checkin_schedule(
            schedule_preferences,
            goal_output
        )
        
        # Create customized check-in content
        for checkin in checkins:
            await self.customize_checkin_content(checkin, goal_output)
        
        return checkins

    def generate_checkin_schedule(self, preferences: CheckinSchedule, goal_output: GoalOutput) -> List[ScheduledCheckin]:
        # Calculate check-in dates
        start_date = datetime.now()
        end_date = start_date + timedelta(weeks=goal_output.timeframe_weeks)
        
        # Create schedule
        checkins = []
        current_date = start_date
        while current_date <= end_date:
            if self.should_schedule_checkin(current_date, preferences):
                checkin = self.create_checkin(current_date, preferences)
                checkins.append(checkin)
            current_date += timedelta(days=1)
        
        return checkins

    async def customize_checkin_content(self, checkin: ScheduledCheckin, goal_output: GoalOutput) -> None:
        # Set required metrics based on goal type
        checkin.metrics_required = self.get_required_metrics(goal_output)
        
        # Generate relevant questions
        checkin.questions = await self.generate_checkin_questions(
            goal_output,
            checkin.checkin_type
        )