from dataclasses import dataclass
from typing import Optional

@dataclass
class UserSessionContext:
    name: str
    uid: int
    age: Optional[int] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    bmi: Optional[float] = None
    goals: List[Dict[str, Any]] = field(default_factory=list)
    progress_history: List[Dict[str, Any]] = field(default_factory=list)
    medical_conditions: List[str] = field(default_factory=list)
    dietary_preferences: List[str] = field(default_factory=list)
    fitness_level: Optional[str] = None
    handoff_logs: List[str] = field(default_factory=list)
    last_checkin: Optional[datetime] = None
    current_streak: int = 0
    achievements: List[str] = field(default_factory=list)