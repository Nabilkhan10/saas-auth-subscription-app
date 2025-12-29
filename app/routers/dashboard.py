from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, Subscription, SubscriptionStatus
from app.auth import get_current_user
from app.schemas import DashboardResponse

templates = Jinja2Templates(directory="app/templates")
router = APIRouter()


@router.get("", response_class=HTMLResponse)
async def dashboard(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """User dashboard"""
    # Get user's subscription
    subscription = db.query(Subscription).filter(
        Subscription.user_id == current_user.id
    ).order_by(Subscription.created_at.desc()).first()

    is_premium = current_user.role.value in ["premium", "admin"]
    
    # Check if subscription is actually active
    if subscription and subscription.status == SubscriptionStatus.ACTIVE:
        is_premium = True
    elif subscription and subscription.status != SubscriptionStatus.ACTIVE:
        is_premium = False

    context = {
        "request": request,
        "user": current_user,
        "subscription": subscription,
        "is_premium": is_premium,
        "upgraded": request.query_params.get("upgraded") == "true"
    }

    return templates.TemplateResponse("dashboard.html", context)

