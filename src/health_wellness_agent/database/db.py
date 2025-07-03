from typing import Optional, List, Any
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from .models import Base, User, Goal, MealPlan, WorkoutPlan, ProgressLog

class Database:
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        self.SessionLocal = sessionmaker(bind=self.engine)

    def create_tables(self) -> None:
        Base.metadata.create_all(self.engine)

    def get_session(self) -> Session:
        return self.SessionLocal()

class DatabaseManager:
    def __init__(self, db: Database):
        self.db = db

    async def create_user(self, user_data: dict) -> User:
        with self.db.get_session() as session:
            user = User(**user_data)
            session.add(user)
            session.commit()
            session.refresh(user)
            return user

    async def get_user(self, user_id: int) -> Optional[User]:
        with self.db.get_session() as session:
            return session.query(User).filter(User.id == user_id).first()

    async def create_goal(self, user_id: int, goal_data: dict) -> Goal:
        with self.db.get_session() as session:
            goal = Goal(user_id=user_id, **goal_data)
            session.add(goal)
            session.commit()
            session.refresh(goal)
            return goal

    async def create_meal_plan(self, user_id: int, plan_data: dict) -> MealPlan:
        with self.db.get_session() as session:
            meal_plan = MealPlan(user_id=user_id, **plan_data)
            session.add(meal_plan)
            session.commit()
            session.refresh(meal_plan)
            return meal_plan

    async def create_workout_plan(self, user_id: int, plan_data: dict) -> WorkoutPlan:
        with self.db.get_session() as session:
            workout_plan = WorkoutPlan(user_id=user_id, **plan_data)
            session.add(workout_plan)
            session.commit()
            session.refresh(workout_plan)
            return workout_plan

    async def log_progress(self, user_id: int, log_data: dict) -> ProgressLog:
        with self.db.get_session() as session:
            progress_log = ProgressLog(user_id=user_id, **log_data)
            session.add(progress_log)
            session.commit()
            session.refresh(progress_log)
            return progress_log

    async def get_user_progress(self, user_id: int, start_date: datetime, end_date: datetime) -> List[ProgressLog]:
        with self.db.get_session() as session:
            return session.query(ProgressLog).filter(
                ProgressLog.user_id == user_id,
                ProgressLog.log_date.between(start_date, end_date)
            ).order_by(ProgressLog.log_date).all()