from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class RoutePoint:
    latitude: float
    longitude: float
    name: str
    type: str  # 'nature', 'urban', 'facility', etc.
    description: str = ""

@dataclass
class Route:
    points: List[RoutePoint]
    distance: float
    duration: int  # in minutes
    difficulty: str  # 'easy', 'moderate', 'hard'
    route_type: str  # 'nature', 'urban', 'quick', 'quiet'
    facilities: List[dict]  # nearby amenities 