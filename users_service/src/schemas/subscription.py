from pydantic import BaseModel


class SubscriptionKeyUpdate(BaseModel):
    subscription_key: str


class SubscribeRequest(BaseModel):
    target_user_id: int
