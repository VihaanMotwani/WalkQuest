from dataclasses import dataclass
from typing import List

@dataclass
class User:
    id: str
    username: str
    email: str
    preferences: dict
    stats: dict  # walking stats
    friends: List[str]  # list of friend IDs
    achievements: List[str] 