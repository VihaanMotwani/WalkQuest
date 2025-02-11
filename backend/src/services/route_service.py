from typing import List, Tuple
from models.route import Route, RoutePoint
from data_processor import LocationData
import math

class RouteService:
    def __init__(self):
        self.location_data = LocationData()
    
    def generate_route(self, 
                      start_point: Tuple[float, float],
                      preferences: dict,
                      desired_length: float) -> Route:
        """Generate a route based on user preferences"""
        route_type = preferences.get('type', 'nature')
        
        if route_type == 'nature':
            points = self._generate_nature_route(start_point, desired_length)
        elif route_type == 'urban':
            points = self._generate_urban_route(start_point, desired_length)
        else:
            points = self._generate_quick_route(start_point, desired_length)
            
        # Calculate route details
        distance = self._calculate_total_distance(points)
        duration = self._estimate_duration(distance)
        difficulty = self._calculate_difficulty(points)
        
        return Route(
            points=points,
            distance=distance,
            duration=duration,
            difficulty=difficulty,
            route_type=route_type,
            facilities=self._find_nearby_facilities(points)
        )

    def _generate_nature_route(self, start_point: Tuple[float, float], desired_length: float) -> List[RoutePoint]:
        """Generate nature-focused route"""
        nature_spots = self.location_data.get_nature_locations()
        route_points = []
        
        # Add start point
        route_points.append(RoutePoint(
            latitude=start_point[0],
            longitude=start_point[1],
            name="Start",
            type="waypoint"
        ))
        
        # Find nearby nature spots
        nearby_spots = []
        for spot in nature_spots:
            dist = self._calculate_distance(start_point, (spot['coordinates'][1], spot['coordinates'][0]))
            if dist <= desired_length/2:  # Within half the desired length
                nearby_spots.append((spot, dist))
        
        # Sort by distance and select points
        nearby_spots.sort(key=lambda x: x[1])
        for spot, _ in nearby_spots[:3]:  # Select up to 3 spots
            route_points.append(RoutePoint(
                latitude=spot['coordinates'][1],
                longitude=spot['coordinates'][0],
                name=spot['name'],
                type='nature',
                description=spot.get('description', '')
            ))
        
        return route_points

    def _calculate_distance(self, point1: Tuple[float, float], point2: Tuple[float, float]) -> float:
        """Calculate distance between two points using Haversine formula"""
        R = 6371  # Earth's radius in kilometers
        
        lat1, lon1 = math.radians(point1[0]), math.radians(point1[1])
        lat2, lon2 = math.radians(point2[0]), math.radians(point2[1])
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        
        return R * c

    def _calculate_total_distance(self, points: List[RoutePoint]) -> float:
        """Calculate total route distance"""
        total = 0
        for i in range(len(points)-1):
            total += self._calculate_distance(
                (points[i].latitude, points[i].longitude),
                (points[i+1].latitude, points[i+1].longitude)
            )
        return total

    def _estimate_duration(self, distance: float) -> int:
        """Estimate walking duration in minutes"""
        avg_walking_speed = 5  # km/h
        return int((distance / avg_walking_speed) * 60)

    def _calculate_difficulty(self, points: List[RoutePoint]) -> str:
        """Calculate route difficulty"""
        distance = self._calculate_total_distance(points)
        if distance < 2:
            return "easy"
        elif distance < 5:
            return "moderate"
        else:
            return "hard"

    def _find_nearby_facilities(self, points: List[RoutePoint]) -> List[dict]:
        """Find facilities near the route"""
        # To be implemented with facilities data
        return [] 