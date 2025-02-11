from typing import List, Tuple
from models.user import User
from models.route import Route

class SocialService:
    def find_nearby_users(self, location: Tuple[float, float]) -> List[User]:
        """Find users within walking distance"""
        pass
    
    def create_group_walk(self, route: Route, creator: User) -> dict:
        """Create a group walking event"""
        pass 