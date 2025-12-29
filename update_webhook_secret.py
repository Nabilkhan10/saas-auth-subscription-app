"""
Update .env file with Stripe Webhook Secret
"""
import os
import re

# Your Stripe Webhook Secret
WEBHOOK_SECRET = "whsec_2ac68399a14d48fee064f4364352e308dc0c6d767bd1a53a28e48a55bf69f9c8"

env_file = ".env"

# Read existing .env file
if os.path.exists(env_file):
    with open(env_file, "r") as f:
        content = f.read()
    
    # Update or add Webhook Secret
    if "STRIPE_WEBHOOK_SECRET=" in content:
        content = re.sub(
            r'STRIPE_WEBHOOK_SECRET=.*',
            f'STRIPE_WEBHOOK_SECRET={WEBHOOK_SECRET}',
            content
        )
    else:
        content += f'\nSTRIPE_WEBHOOK_SECRET={WEBHOOK_SECRET}'
    
    # Write back to file
    with open(env_file, "w") as f:
        f.write(content)
    
    print("[SUCCESS] Updated .env with Stripe Webhook Secret!")
    print(f"Webhook Secret: {WEBHOOK_SECRET[:20]}...")
    print("\nYour Stripe integration is now COMPLETE!")
    print("\nYou can now:")
    print("1. Start the app: uvicorn app.main:app --reload")
    print("2. Test the full payment flow with test card: 4242 4242 4242 4242")
else:
    print("[ERROR] .env file not found. Run setup_env.py first.")

