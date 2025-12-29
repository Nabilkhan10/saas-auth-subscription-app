from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, UserRole
from app.schemas import UserRegister, UserLogin, Token, UserResponse
from app.auth import (
    get_password_hash,
    authenticate_user,
    create_access_token,
    get_user_by_email,
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")
router = APIRouter()


@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """Registration page"""
    return templates.TemplateResponse("auth/register.html", {"request": request})


@router.post("/register", response_class=HTMLResponse)
async def register(
    request: Request,
    db: Session = Depends(get_db)
):
    """Register a new user"""
    form = await request.form()
    email = form.get("email")
    password = form.get("password")
    
    if not email or not password:
        return templates.TemplateResponse(
            "auth/register.html",
            {"request": request, "error": "Email and password are required"},
            status_code=400
        )
    
    # Check if user already exists
    existing_user = get_user_by_email(db, email)
    if existing_user:
        return templates.TemplateResponse(
            "auth/register.html",
            {"request": request, "error": "Email already registered"},
            status_code=400
        )

    # Create new user
    hashed_password = get_password_hash(password)
    new_user = User(
        email=email,
        password_hash=hashed_password,
        role=UserRole.FREE
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Auto-login after registration
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": new_user.email}, expires_delta=access_token_expires
    )

    response = RedirectResponse(url="/dashboard", status_code=303)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite="lax"
    )
    return response


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Login page"""
    return templates.TemplateResponse("auth/login.html", {"request": request})


@router.post("/login", response_class=HTMLResponse)
async def login(
    request: Request,
    db: Session = Depends(get_db)
):
    """Login user"""
    form = await request.form()
    email = form.get("username") or form.get("email")
    password = form.get("password")
    
    if not email or not password:
        return templates.TemplateResponse(
            "auth/login.html",
            {"request": request, "error": "Email and password are required"},
            status_code=401
        )
    
    user = authenticate_user(db, email, password)
    if not user:
        return templates.TemplateResponse(
            "auth/login.html",
            {"request": request, "error": "Incorrect email or password"},
            status_code=401
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    response = RedirectResponse(url="/dashboard", status_code=303)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite="lax"
    )
    return response


@router.get("/logout")
async def logout():
    """Logout user"""
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie(key="access_token")
    return response


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return current_user

