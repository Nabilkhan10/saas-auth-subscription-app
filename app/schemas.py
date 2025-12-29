from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from app.models import UserRole, SubscriptionStatus


# Auth schemas
class UserRegister(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


# User schemas
class UserResponse(BaseModel):
    id: int
    email: str
    role: UserRole
    is_verified: bool
    created_at: datetime

    class Config:
        from_attributes = True


# Subscription schemas
class SubscriptionResponse(BaseModel):
    id: int
    user_id: int
    status: SubscriptionStatus
    plan_name: Optional[str]
    current_period_end: Optional[datetime]
    cancel_at_period_end: bool

    class Config:
        from_attributes = True


class DashboardResponse(BaseModel):
    user: UserResponse
    subscription: Optional[SubscriptionResponse] = None
    is_premium: bool

