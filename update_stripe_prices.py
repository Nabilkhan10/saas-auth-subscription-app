"""
Update .env file with Stripe Price IDs
Usage: Edit this file to add your Price IDs, then run: python update_stripe_prices.py
"""

import os
import re

# Add your Stripe Price IDs here (get them from Stripe Dashboard)
MONTHLY_PRICE_ID = "price_your_monthly_price_id_here"
ANNUAL_PRICE_ID = "price_your_annual_price_id_here"

env_file = ".env"

# Read existing .env file
if os.path.exists(env_file):
    with open(env_file, "r") as f:
        content = f.read()

    # Update or add Monthly Price ID
    if "STRIPE_MONTHLY_PRICE_ID=" in content:
        content = re.sub(
            r"STRIPE_MONTHLY_PRICE_ID=.*",
            f"STRIPE_MONTHLY_PRICE_ID={MONTHLY_PRICE_ID}",
            content,
        )
    else:
        content += f"\nSTRIPE_MONTHLY_PRICE_ID={MONTHLY_PRICE_ID}"

    # Update or add Annual Price ID
    if "STRIPE_ANNUAL_PRICE_ID=" in content:
        content = re.sub(
            r"STRIPE_ANNUAL_PRICE_ID=.*",
            f"STRIPE_ANNUAL_PRICE_ID={ANNUAL_PRICE_ID}",
            content,
        )
    else:
        content += f"\nSTRIPE_ANNUAL_PRICE_ID={ANNUAL_PRICE_ID}"

    # Write back to file
    with open(env_file, "w") as f:
        f.write(content)

    print("[SUCCESS] Updated .env with Stripe Price IDs!")
    print(f"Monthly Price ID: {MONTHLY_PRICE_ID}")
    print(f"Annual Price ID: {ANNUAL_PRICE_ID}")
    print("\nYour Stripe integration is now fully configured!")
else:
    print("[ERROR] .env file not found. Run setup_env.py first.")
