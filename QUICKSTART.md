# 🚀 Quick Start Guide

Get your SaaS app running in 5 minutes!

## Step 1: Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

## Step 2: Set Up Environment

Create a `.env` file:

```bash
# Copy the example
cp .env.example .env
```

Edit `.env` and add at minimum:

```env
SECRET_KEY=change-this-to-a-random-string
DATABASE_URL=sqlite:///./saas_app.db
```

**Generate a secret key:**
```python
import secrets
print(secrets.token_urlsafe(32))
```

## Step 3: Run the App

```bash
uvicorn app.main:app --reload
```

Visit http://localhost:8000

## Step 4: Test Without Stripe (Optional)

You can test the app without Stripe by:
1. Registering a user
2. Logging in
3. Viewing the dashboard

Stripe features require Stripe API keys (see main README.md).

## 🎯 Next Steps

- Read the full [README.md](README.md) for Stripe setup
- Customize the UI in `app/templates/`
- Add your own features!

---

**Troubleshooting:**

- **Import errors?** Make sure virtual environment is activated
- **Database errors?** Delete `saas_app.db` and restart
- **Port in use?** Change port: `uvicorn app.main:app --reload --port 8001`

