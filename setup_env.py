"""
Setup script to create .env file
Run this script to automatically create your .env file
"""

import os
import secrets

# Generate a secure secret key
SECRET_KEY = secrets.token_urlsafe(32)

env_content = f"""# Database
DATABASE_URL=sqlite:///./saas_app.db

# JWT Secret (auto-generated secure key)
SECRET_KEY={SECRET_KEY}

# Stripe Keys (Test Mode) - Add your keys from Stripe Dashboard
STRIPE_PUBLISHABLE_KEY=pk_test_your_publishable_key_here
STRIPE_SECRET_KEY=sk_test_your_secret_key_here
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret_here

# Stripe Price IDs (create products in Stripe dashboard and add IDs here)
# Get these from: https://dashboard.stripe.com/test/products
STRIPE_MONTHLY_PRICE_ID=price_your_monthly_price_id
STRIPE_ANNUAL_PRICE_ID=price_your_annual_price_id

# App Settings
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
BASE_URL=http://localhost:8000
"""

# Write .env file
with open(".env", "w") as f:
    f.write(env_content)

print("[SUCCESS] .env file created successfully!")
print("\nNext steps:")
print(
    "1. Create products in Stripe Dashboard: https://dashboard.stripe.com/test/products"
)
print(
    "2. Copy the Price IDs and update STRIPE_MONTHLY_PRICE_ID and STRIPE_ANNUAL_PRICE_ID in .env"
)
print("3. Set up webhook (see STRIPE_SETUP.md for details)")
print("\nThen run: uvicorn app.main:app --reload")
