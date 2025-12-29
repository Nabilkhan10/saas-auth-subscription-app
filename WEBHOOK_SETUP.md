# 🔗 How to Get Webhook Secret from Stripe Dashboard

Follow these steps to get your webhook secret manually from the Stripe website:

## 📋 Step-by-Step Instructions

### Step 1: Go to Stripe Dashboard

1. Open https://dashboard.stripe.com/test/webhooks
2. Make sure you're in **Test mode** (toggle in top right should say "Test mode")

### Step 2: Add Webhook Endpoint

1. Click the **"+ Add endpoint"** button (top right)
2. You'll see a form to create a new webhook endpoint

### Step 3: Configure the Endpoint

**For Local Development (using ngrok or similar):**
- **Endpoint URL**: `https://your-ngrok-url.ngrok.io/billing/webhook`
  - Or use a service like ngrok to expose your localhost
  - Example: If using ngrok: `ngrok http 8000` then use the HTTPS URL

**For Production:**
- **Endpoint URL**: `https://your-domain.com/billing/webhook`
  - Replace `your-domain.com` with your actual domain

### Step 4: Select Events to Listen To

In the "Events to send" section, select these events:

✅ **checkout.session.completed** - When a checkout is completed
✅ **customer.subscription.updated** - When subscription status changes
✅ **customer.subscription.deleted** - When subscription is canceled

You can either:
- Click "Select events" and choose individual events
- Or use "Send all events" (not recommended for production)

### Step 5: Create the Endpoint

1. Click **"Add endpoint"** button
2. The webhook endpoint will be created

### Step 6: Get the Webhook Secret

1. After creating, you'll see the webhook endpoint details page
2. Look for **"Signing secret"** section
3. Click **"Reveal"** or **"Click to reveal"** button
4. Copy the secret (it starts with `whsec_...`)
   - Example: `whsec_1234567890abcdef...`

### Step 7: Add to Your .env File

1. Open your `.env` file
2. Find the line: `STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret_here`
3. Replace `whsec_your_webhook_secret_here` with your actual secret:
   ```
   STRIPE_WEBHOOK_SECRET=whsec_1234567890abcdef...
   ```
4. Save the file

## 🧪 Testing Your Webhook

### For Local Development

Since Stripe can't reach `localhost`, you have two options:

#### Option A: Use Stripe CLI (Easier)
```bash
stripe listen --forward-to localhost:8000/billing/webhook
```
This automatically forwards webhooks to your local server.

#### Option B: Use ngrok (For Manual Testing)
1. Install ngrok: https://ngrok.com/
2. Run: `ngrok http 8000`
3. Copy the HTTPS URL (e.g., `https://abc123.ngrok.io`)
4. Use this URL in Stripe dashboard: `https://abc123.ngrok.io/billing/webhook`
5. Get the webhook secret from Stripe dashboard

### For Production

1. Deploy your app to a server (Railway, Render, etc.)
2. Use your production URL in the webhook endpoint
3. Get the webhook secret from Stripe dashboard
4. Add it to your production environment variables

## 📸 Visual Guide

The webhook secret will look like this in the Stripe dashboard:

```
Signing secret
whsec_1234567890abcdefghijklmnopqrstuvwxyz
[Click to reveal] [Copy]
```

## ✅ Verification

After setting up:

1. Make a test purchase in your app
2. Go to Stripe Dashboard → Webhooks
3. Click on your webhook endpoint
4. Check the "Events" tab
5. You should see events being received:
   - `checkout.session.completed`
   - `customer.subscription.updated`

## 🔒 Security Notes

- ⚠️ **Never commit** your webhook secret to Git
- ✅ Keep it in `.env` file (already in `.gitignore`)
- ✅ Use different secrets for test and production
- ✅ Rotate secrets if accidentally exposed

## 🆘 Troubleshooting

**Problem**: Webhook not receiving events
- ✅ Check that your endpoint URL is correct
- ✅ Verify events are selected in Stripe dashboard
- ✅ Make sure your server is running and accessible
- ✅ Check server logs for errors

**Problem**: "Invalid signature" error
- ✅ Verify webhook secret in `.env` matches Stripe dashboard
- ✅ Make sure you're using the correct secret (test vs live)
- ✅ Check that the webhook secret starts with `whsec_`

---

**Need help?** Check the main [README.md](README.md) for more details.

