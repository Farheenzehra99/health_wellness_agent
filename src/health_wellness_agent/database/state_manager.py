from typing import Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class SessionState(Base):
    __tablename__ = 'session_states'
    
    id = Column(Integer, primary_key=True)
    session_id = Column(String, unique=True)
    user_context = Column(JSON)
    conversation_state = Column(JSON)
    last_updated = Column(DateTime, default=datetime.utcnow)

class StateManager:
    def __init__(self, database_url: str):
        self.engine = create_async_engine(database_url)
        self.SessionLocal = sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    async def save_state(self, session_id: str, context: Dict[str, Any]) -> None:
        async with self.SessionLocal() as session:
            state = SessionState(
                session_id=session_id,
                user_context=context,
                last_updated=datetime.utcnow()
            )
            session.add(state)
            await session.commit()

    async def load_state(self, session_id: str) -> Optional[Dict[str, Any]]:
        async with self.SessionLocal() as session:
            result = await session.get(SessionState, session_id)
            return result.user_context if result else None

    async def update_state(self, session_id: str, updates: Dict[str, Any]) -> None:
        async with self.SessionLocal() as session:
            state = await session.get(SessionState, session_id)
            if state:
                state.user_context.update(updates)
                state.last_updated = datetime.utcnow()
                await session.commit()