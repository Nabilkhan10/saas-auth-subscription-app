from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

from app.database import engine, Base
from app.routers import auth, billing, dashboard, premium

load_dotenv()

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SaaS Auth & Subscription App",
    description="Full-stack SaaS application with authentication, role-based access, and Stripe billing",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files and templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(billing.router, prefix="/billing", tags=["Billing"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
app.include_router(premium.router, prefix="/premium", tags=["Premium"])


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Home page"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}

