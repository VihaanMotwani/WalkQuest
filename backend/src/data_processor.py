import json
from typing import Dict, List, Optional

class LocationData:
    def __init__(self):
        self.tourist_attractions = self._load_geojson("backend/src/data/TouristAttractions.geojson")
        self.parks = self._load_geojson("backend/src/data/ParksSG.geojson")
        self.nature_reserves = self._load_geojson("backend/src/data/NParksParksandNatureReserves.geojson")

    def _load_geojson(self, filepath: str) -> Dict:
        """Load and parse a GeoJSON file"""
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading {filepath}: {e}")
            return {"type": "FeatureCollection", "features": []}

    def get_nature_locations(self) -> List[Dict]:
        """Get all parks and nature reserves"""
        nature_spots = []
        
        # Add parks
        for feature in self.parks["features"]:
            if feature["properties"].get("NAME"):
                nature_spots.append({
                    "name": feature["properties"]["NAME"],
                    "type": "park",
                    "coordinates": feature["geometry"]["coordinates"],
                    "description": feature["properties"].get("DESCRIPTION", ""),
                    "address": feature["properties"].get("ADDRESSSTREETNAME", "")
                })

        # Add nature reserves
        for feature in self.nature_reserves["features"]:
            # Process nature reserve features here
            pass

        return nature_spots

    def get_tourist_attractions(self) -> List[Dict]:
        """Get tourist attractions"""
        attractions = []
        
        for feature in self.tourist_attractions["features"]:
            props = feature["properties"]
            if props.get("PAGETITLE"):
                attractions.append({
                    "name": props["PAGETITLE"],
                    "type": "attraction",
                    "coordinates": feature["geometry"]["coordinates"],
                    "overview": props.get("OVERVIEW", ""),
                    "address": props.get("ADDRESS", "")
                })

        return attractions 