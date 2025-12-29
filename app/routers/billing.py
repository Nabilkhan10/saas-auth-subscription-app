import stripe
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse, JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime
import os
from dotenv import load_dotenv

from app.database import get_db
from app.models import User, Subscription, SubscriptionStatus
from app.auth import get_current_user
from app.models import UserRole

load_dotenv()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

router = APIRouter()


@router.get("/checkout")
async def create_checkout_session(
    plan: str = "monthly",  # monthly or annual
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create Stripe checkout session"""
    if plan not in ["monthly", "annual"]:
        raise HTTPException(status_code=400, detail="Invalid plan")

    # Define prices (in cents) - replace with your actual Stripe price IDs
    prices = {
        "monthly": os.getenv("STRIPE_MONTHLY_PRICE_ID", "price_monthly"),
        "annual": os.getenv("STRIPE_ANNUAL_PRICE_ID", "price_annual")
    }

    price_id = prices.get(plan)
    if not price_id:
        raise HTTPException(status_code=500, detail="Price ID not configured")

    try:
        # Create or get Stripe customer
        if not current_user.stripe_customer_id:
            customer = stripe.Customer.create(
                email=current_user.email,
                metadata={"user_id": str(current_user.id)}
            )
            current_user.stripe_customer_id = customer.id
            db.commit()

        # Create checkout session
        checkout_session = stripe.checkout.Session.create(
            customer=current_user.stripe_customer_id,
            payment_method_types=["card"],
            line_items=[{
                "price": price_id,
                "quantity": 1,
            }],
            mode="subscription",
            success_url=f"{os.getenv('BASE_URL', 'http://localhost:8000')}/billing/success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{os.getenv('BASE_URL', 'http://localhost:8000')}/dashboard",
            metadata={"user_id": str(current_user.id), "plan": plan}
        )

        return RedirectResponse(url=checkout_session.url, status_code=303)

    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/success")
async def checkout_success(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Handle successful checkout"""
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        if session.customer != current_user.stripe_customer_id:
            raise HTTPException(status_code=403, detail="Unauthorized")

        # Redirect to dashboard - webhook will handle subscription creation
        return RedirectResponse(url="/dashboard?upgraded=true", status_code=303)
    except stripe.error.StripeError:
        raise HTTPException(status_code=400, detail="Invalid session")


@router.post("/webhook")
async def stripe_webhook(
    request: Request,
    db: Session = Depends(get_db)
):
    """Handle Stripe webhooks"""
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    # Handle different event types
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        user_id = int(session["metadata"]["user_id"])
        user = db.query(User).filter(User.id == user_id).first()
        
        if user:
            # Get subscription from Stripe
            subscription_id = session.get("subscription")
            if subscription_id:
                subscription = stripe.Subscription.retrieve(subscription_id)
                
                # Create or update subscription in database
                db_subscription = db.query(Subscription).filter(
                    Subscription.stripe_subscription_id == subscription_id
                ).first()
                
                if not db_subscription:
                    db_subscription = Subscription(
                        user_id=user.id,
                        stripe_subscription_id=subscription_id,
                        status=SubscriptionStatus.ACTIVE,
                        plan_name=session["metadata"].get("plan", "monthly"),
                        current_period_end=datetime.fromtimestamp(subscription.current_period_end),
                    )
                    db.add(db_subscription)
                else:
                    db_subscription.status = SubscriptionStatus.ACTIVE
                    db_subscription.current_period_end = datetime.fromtimestamp(subscription.current_period_end)
                
                # Update user role to premium
                user.role = UserRole.PREMIUM
                db.commit()

    elif event["type"] == "customer.subscription.updated":
        subscription = event["data"]["object"]
        db_subscription = db.query(Subscription).filter(
            Subscription.stripe_subscription_id == subscription.id
        ).first()
        
        if db_subscription:
            db_subscription.status = SubscriptionStatus(subscription.status)
            db_subscription.current_period_end = datetime.fromtimestamp(subscription.current_period_end)
            db_subscription.cancel_at_period_end = subscription.cancel_at_period_end
            
            # Update user role based on subscription status
            user = db_subscription.user
            if subscription.status == "active":
                user.role = UserRole.PREMIUM
            elif subscription.status in ["canceled", "past_due", "unpaid"]:
                user.role = UserRole.FREE
            
            db.commit()

    elif event["type"] == "customer.subscription.deleted":
        subscription = event["data"]["object"]
        db_subscription = db.query(Subscription).filter(
            Subscription.stripe_subscription_id == subscription.id
        ).first()
        
        if db_subscription:
            db_subscription.status = SubscriptionStatus.CANCELED
            db_subscription.user.role = UserRole.FREE
            db.commit()

    return JSONResponse({"status": "success"})


@router.post("/cancel")
async def cancel_subscription(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Cancel user's subscription"""
    subscription = db.query(Subscription).filter(
        Subscription.user_id == current_user.id,
        Subscription.status == SubscriptionStatus.ACTIVE
    ).first()

    if not subscription:
        raise HTTPException(status_code=404, detail="No active subscription found")

    try:
        stripe_subscription = stripe.Subscription.retrieve(subscription.stripe_subscription_id)
        stripe.Subscription.modify(
            subscription.stripe_subscription_id,
            cancel_at_period_end=True
        )
        
        subscription.cancel_at_period_end = True
        db.commit()
        
        return {"message": "Subscription will be canceled at the end of the billing period"}
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))

