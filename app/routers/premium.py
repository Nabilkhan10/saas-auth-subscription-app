from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, UserRole, Subscription, SubscriptionStatus
from app.auth import get_current_user, require_role

templates = Jinja2Templates(directory="app/templates")
router = APIRouter()


@router.get("/features", response_class=HTMLResponse)
async def premium_features(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Premium features page - accessible to premium users only"""
    # Check if user has active premium subscription
    subscription = db.query(Subscription).filter(
        Subscription.user_id == current_user.id,
        Subscription.status == SubscriptionStatus.ACTIVE
    ).first()

    is_premium = (
        current_user.role in [UserRole.PREMIUM, UserRole.ADMIN] or
        (subscription and subscription.status == SubscriptionStatus.ACTIVE)
    )

    if not is_premium:
        return templates.TemplateResponse(
            "premium/locked.html",
            {
                "request": request,
                "user": current_user,
                "message": "This feature is only available for premium users."
            },
            status_code=403
        )

    return templates.TemplateResponse(
        "premium/features.html",
        {
            "request": request,
            "user": current_user,
            "subscription": subscription
        }
    )


@router.get("/api/data")
async def premium_api_data(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Premium API endpoint - returns data only for premium users"""
    subscription = db.query(Subscription).filter(
        Subscription.user_id == current_user.id,
        Subscription.status == SubscriptionStatus.ACTIVE
    ).first()

    is_premium = (
        current_user.role in [UserRole.PREMIUM, UserRole.ADMIN] or
        (subscription and subscription.status == SubscriptionStatus.ACTIVE)
    )

    if not is_premium:
        raise HTTPException(
            status_code=403,
            detail="Premium subscription required"
        )

    return {
        "message": "Welcome to premium features!",
        "data": {
            "advanced_analytics": True,
            "api_access": True,
            "priority_support": True,
            "exclusive_content": "This is premium-only content!"
        }
    }

