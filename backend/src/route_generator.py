from typing import List, Dict, Tuple
from math import radians, sin, cos, sqrt, atan2

class RouteGenerator:
    def __init__(self, location_data):
        self.location_data = location_data

    def calculate_distance(self, coord1: Tuple[float, float], 
                         coord2: Tuple[float, float]) -> float:
        """Calculate distance between two coordinates using Haversine formula"""
        R = 6371  # Earth's radius in kilometers

        lat1, lon1 = radians(coord1[1]), radians(coord1[0])
        lat2, lon2 = radians(coord2[1]), radians(coord2[0])

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        distance = R * c

        return distance

    def generate_nature_route(self, start_coord: Tuple[float, float], 
                            desired_length: float) -> List[Dict]:
        """Generate a nature-focused walking route"""
        nature_spots = self.location_data.get_nature_locations()
        route = []
        
        # Find nearby nature spots within desired distance
        for spot in nature_spots:
            spot_coord = (spot["coordinates"][0], spot["coordinates"][1])
            distance = self.calculate_distance(start_coord, spot_coord)
            
            if distance <= desired_length:
                spot["distance_from_start"] = distance
                route.append(spot)

        # Sort by distance from start
        route.sort(key=lambda x: x["distance_from_start"])
        
        return route[:5]  # Return top 5 closest spots 