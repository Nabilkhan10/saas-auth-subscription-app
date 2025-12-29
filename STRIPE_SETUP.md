# 🔑 Stripe Setup Guide

Your Stripe test keys have been added to `.env`! Here's what you need to do next:

## ✅ What's Already Done

- ✅ Secret Key: `sk_test_OD2vxsEFjPWJSKxw7xyPKkGo00uV6vxNLU`
- ✅ Publishable Key: `pk_test_pOpwThyuoDpxHctEcOdoklBd00UBxLfPQo`

## 📋 Next Steps

### 1. Create Products & Prices in Stripe

1. Go to https://dashboard.stripe.com/test/products
2. Click **"+ Add product"**

#### Create Monthly Plan:
- **Name**: "Monthly Premium"
- **Pricing model**: Recurring
- **Price**: $9.99/month (or your choice)
- **Billing period**: Monthly
- **Copy the Price ID** (starts with `price_...`)
- Add to `.env` as `STRIPE_MONTHLY_PRICE_ID`

#### Create Annual Plan:
- **Name**: "Annual Premium"
- **Pricing model**: Recurring
- **Price**: $99/year (or your choice)
- **Billing period**: Yearly
- **Copy the Price ID** (starts with `price_...`)
- Add to `.env` as `STRIPE_ANNUAL_PRICE_ID`

### 2. Set Up Webhooks (For Local Development)

#### Option A: Using Stripe CLI (Recommended for Testing)

1. **Install Stripe CLI**: https://stripe.com/docs/stripe-cli

2. **Login to Stripe**:
   ```bash
   stripe login
   ```

3. **Forward webhooks to local server**:
   ```bash
   stripe listen --forward-to localhost:8000/billing/webhook
   ```

4. **Copy the webhook signing secret** (starts with `whsec_...`)
   - It will be displayed in the terminal output
   - Add it to `.env` as `STRIPE_WEBHOOK_SECRET`

#### Option B: Using Stripe Dashboard (For Production)

1. Go to https://dashboard.stripe.com/test/webhooks
2. Click **"+ Add endpoint"**
3. **Endpoint URL**: `https://your-domain.com/billing/webhook`
4. **Events to send**:
   - `checkout.session.completed`
   - `customer.subscription.updated`
   - `customer.subscription.deleted`
5. Copy the **Signing secret** and add to `.env`

### 3. Update .env File

After creating products, your `.env` should look like:

```env
STRIPE_MONTHLY_PRICE_ID=price_1ABC123xyz...
STRIPE_ANNUAL_PRICE_ID=price_1DEF456abc...
STRIPE_WEBHOOK_SECRET=whsec_xyz123...
```

## 🧪 Testing

### Test Cards (Stripe Test Mode)

Use these cards to test payments:

| Card Number | Result |
|-------------|--------|
| `4242 4242 4242 4242` | ✅ Success |
| `4000 0000 0000 0002` | ❌ Card declined |
| `4000 0000 0000 9995` | ❌ Insufficient funds |

**For all test cards:**
- **Expiry**: Any future date (e.g., 12/25)
- **CVC**: Any 3 digits (e.g., 123)
- **ZIP**: Any 5 digits (e.g., 12345)

### Test Flow

1. Start your app: `uvicorn app.main:app --reload`
2. Register a new user
3. Go to dashboard
4. Click "Upgrade to Premium"
5. Use test card: `4242 4242 4242 4242`
6. Complete checkout
7. Webhook should update user role to `premium`

## 🔒 Security Notes

⚠️ **Important:**
- These are **test keys** - safe to use in development
- **Never commit** `.env` to Git (already in `.gitignore`)
- For production, use **live keys** from Stripe Dashboard
- Rotate keys if accidentally exposed

## 🚀 You're Ready!

Once you've:
1. ✅ Created products in Stripe
2. ✅ Added Price IDs to `.env`
3. ✅ Set up webhook (Stripe CLI or Dashboard)

Your app is ready to test payments! 🎉

---

**Need help?** Check the main [README.md](README.md) for more details.

