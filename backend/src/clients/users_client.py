"""HTTP client for communication with users-service."""
import httpx
from typing import Optional, Dict, Any


class UsersClient:
    def __init__(self, base_url: str = "http://users-api:8000"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(base_url=base_url, timeout=5.0)
    
    async def close(self):
        await self.client.aclose()
    
    async def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        try:
            response = await self.client.get(f"/api/users/{user_id}")
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return None
            else:
                response.raise_for_status()
                
        except httpx.HTTPError as e:
            print(f"Error fetching user {user_id}: {e}")
            return None
    
    async def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        try:
            response = await self.client.get(
                "/api/user",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return None
                
        except httpx.HTTPError:
            return None


users_client = UsersClient()
