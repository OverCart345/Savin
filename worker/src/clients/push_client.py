import httpx

from core.config import settings


class PushNotificationClient:
    
    def __init__(self):
        self.push_url = settings.push_url
        self._client = None
    
    async def get_client(self):
        if not self._client:
            self._client = httpx.AsyncClient(timeout=10.0)
        return self._client
    
    async def close(self):
        if self._client:
            await self._client.aclose()
            self._client = None
    
    async def send_notification(
        self, 
        subscription_key: str, 
        message: str
    ) -> bool:
        
        client = await self.get_client()
        
        try:
            response = await client.post(
                self.push_url,
                headers={
                    "Authorization": f"Bearer {subscription_key}",
                    "Content-Type": "application/json"
                },
                json={"message": message}
            )
            
            if response.status_code in [200, 201, 204]:
                return True
            else:
                print(f"Push notification failed: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"Error sending push notification: {e}")
            return False
