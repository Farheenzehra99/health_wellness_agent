from datetime import datetime
from typing import List, Optional
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    age = Column(Integer)
    gender = Column(String(20))
    height = Column(Float)
    weight = Column(Float)
    medical_conditions = Column(JSON)
    allergies = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    goals = relationship('Goal', back_populates='user')
    meal_plans = relationship('MealPlan', back_populates='user')
    workout_plans = relationship('WorkoutPlan', back_populates='user')
    progress_logs = relationship('ProgressLog', back_populates='user')

class Goal(Base):
    __tablename__ = 'goals'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    goal_type = Column(String(50), nullable=False)
    target_value = Column(Float, nullable=False)
    timeframe_weeks = Column(Integer, nullable=False)
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime)
    metrics = Column(JSON)
    constraints = Column(JSON)
    status = Column(String(20), default='active')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship('User', back_populates='goals')

class MealPlan(Base):
    __tablename__ = 'meal_plans'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    daily_plans = Column(JSON)
    nutritional_info = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship('User', back_populates='meal_plans')

class WorkoutPlan(Base):
    __tablename__ = 'workout_plans'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    weekly_schedule = Column(JSON)
    progression_plan = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship('User', back_populates='workout_plans')

class ProgressLog(Base):
    __tablename__ = 'progress_logs'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    log_date = Column(DateTime, nullable=False)
    weight = Column(Float)
    measurements = Column(JSON)
    energy_level = Column(Integer)
    workout_compliance = Column(Float)
    diet_compliance = Column(Float)
    notes = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship('User', back_populates='progress_logs')