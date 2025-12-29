# 💎 SaaS Auth & Subscription App

A full-stack FastAPI web application demonstrating real-world SaaS engineering with user authentication, role-based access control, and Stripe subscription billing.

## 🎯 Features

- ✅ **Secure Authentication** - JWT-based auth with password hashing
- ✅ **User Roles** - Free, Premium, and Admin roles
- ✅ **Stripe Integration** - Subscription checkout and webhook handling
- ✅ **Protected Routes** - Role-based access control
- ✅ **Dashboard** - Subscription management and billing info
- ✅ **Modern UI** - Beautiful Tailwind CSS interface

## 🏗️ Tech Stack

- **Backend**: FastAPI
- **Database**: SQLite (easily switchable to PostgreSQL)
- **Authentication**: JWT tokens with bcrypt password hashing
- **Payments**: Stripe API
- **Frontend**: Jinja2 templates + Tailwind CSS
- **ORM**: SQLAlchemy

## 📦 Installation

### 1. Clone and Setup

```bash
# Navigate to project directory
cd "saas-auth-subscription-app"

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Configuration

Create a `.env` file in the root directory:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
# Database
DATABASE_URL=sqlite:///./saas_app.db

# JWT Secret (generate a random string)
SECRET_KEY=your-super-secret-key-change-this-in-production

# Stripe Keys (get from https://dashboard.stripe.com/test/apikeys)
STRIPE_PUBLISHABLE_KEY=pk_test_your_publishable_key
STRIPE_SECRET_KEY=sk_test_your_secret_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret

# Stripe Price IDs (create products in Stripe dashboard)
STRIPE_MONTHLY_PRICE_ID=price_your_monthly_price_id
STRIPE_ANNUAL_PRICE_ID=price_your_annual_price_id

# App Settings
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
BASE_URL=http://localhost:8000
```

### 3. Stripe Setup

1. **Create a Stripe Account** (use test mode for development)
   - Go to https://stripe.com and create an account
   - Navigate to Developers → API keys
   - Copy your test keys to `.env`

2. **Create Products and Prices**
   - Go to Products in Stripe Dashboard
   - Create two products: "Monthly Premium" and "Annual Premium"
   - Create recurring prices for each (monthly/annual)
   - Copy the Price IDs to `.env` as `STRIPE_MONTHLY_PRICE_ID` and `STRIPE_ANNUAL_PRICE_ID`

3. **Set up Webhooks** (for production)
   - Go to Developers → Webhooks
   - Add endpoint: `https://your-domain.com/billing/webhook`
   - Select events: `checkout.session.completed`, `customer.subscription.updated`, `customer.subscription.deleted`
   - Copy webhook signing secret to `.env` as `STRIPE_WEBHOOK_SECRET`

   **For local development**, use Stripe CLI:
   ```bash
   # Install Stripe CLI: https://stripe.com/docs/stripe-cli
   stripe listen --forward-to localhost:8000/billing/webhook
   # Copy the webhook secret from the output
   ```

## 🚀 Running the Application

```bash
# Make sure virtual environment is activated
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Visit http://localhost:8000 in your browser.

## 📁 Project Structure

```
Project 4/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry point
│   ├── database.py          # Database configuration
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── auth.py              # Authentication utilities
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py          # Auth routes (register, login, logout)
│   │   ├── billing.py       # Stripe billing routes
│   │   ├── dashboard.py     # User dashboard
│   │   └── premium.py       # Premium features
│   ├── templates/           # Jinja2 HTML templates
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── dashboard.html
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   └── premium/
│   │       ├── features.html
│   │       └── locked.html
│   └── static/              # Static files (CSS, JS, images)
├── requirements.txt
├── .env.example
└── README.md
```

## 🔐 Authentication Flow

1. User registers → Password is hashed with bcrypt
2. JWT token is created and stored in HTTP-only cookie
3. Protected routes check for valid token
4. Token expires after 30 minutes (configurable)

## 💳 Stripe Integration Flow

1. User clicks "Upgrade to Premium"
2. Backend creates Stripe Checkout session
3. User completes payment on Stripe
4. Stripe sends webhook to `/billing/webhook`
5. Backend updates user role to `premium`
6. User gains access to premium features

## 🧪 Testing

### Test User Flow

1. **Register**: Go to `/auth/register` and create an account
2. **Login**: Sign in at `/auth/login`
3. **Dashboard**: View your account at `/dashboard`
4. **Upgrade**: Click "Upgrade to Premium" (use Stripe test card: `4242 4242 4242 4242`)
5. **Premium Features**: Access `/premium/features` after upgrade

### Stripe Test Cards

- **Success**: `4242 4242 4242 4242`
- **Decline**: `4000 0000 0000 0002`
- Use any future expiry date and any CVC

## 🚢 Deployment

### Railway

1. Push code to GitHub
2. Create new project on Railway
3. Connect GitHub repository
4. Add environment variables from `.env`
5. Deploy!

### Render

1. Create new Web Service
2. Connect GitHub repository
3. Build command: `pip install -r requirements.txt`
4. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables
6. Deploy!

### Important for Production

- ✅ Change `SECRET_KEY` to a strong random string
- ✅ Use PostgreSQL instead of SQLite
- ✅ Set `BASE_URL` to your production domain
- ✅ Configure Stripe webhook endpoint
- ✅ Enable HTTPS
- ✅ Set secure cookie flags (`secure=True`, `samesite="lax"`)

## 📊 Database Schema

### Users Table
- `id` - Primary key
- `email` - Unique email address
- `password_hash` - Bcrypt hashed password
- `role` - Enum: free, premium, admin
- `stripe_customer_id` - Stripe customer ID
- `is_verified` - Email verification status
- `created_at` - Account creation timestamp

### Subscriptions Table
- `id` - Primary key
- `user_id` - Foreign key to users
- `stripe_subscription_id` - Stripe subscription ID
- `status` - Enum: active, canceled, past_due, etc.
- `plan_name` - monthly or annual
- `current_period_end` - Next billing date
- `cancel_at_period_end` - Cancellation flag

## 🔒 Security Features

- Password hashing with bcrypt
- JWT token authentication
- HTTP-only cookies
- Role-based access control
- Stripe webhook signature verification
- SQL injection protection (SQLAlchemy ORM)

## 🎨 Customization

### Change App Theme

Edit `app/templates/base.html` and update Tailwind classes.

### Add More Roles

1. Add new role to `UserRole` enum in `app/models.py`
2. Update `require_role()` usage in routes
3. Add role-specific features

### Add More Subscription Plans

1. Create new product in Stripe
2. Add price ID to `.env`
3. Update checkout route in `app/routers/billing.py`

## 📝 API Endpoints

- `GET /` - Home page
- `GET /auth/register` - Registration page
- `POST /auth/register` - Create account
- `GET /auth/login` - Login page
- `POST /auth/login` - Authenticate user
- `GET /auth/logout` - Logout user
- `GET /dashboard` - User dashboard
- `GET /billing/checkout?plan=monthly` - Stripe checkout
- `POST /billing/webhook` - Stripe webhook handler
- `POST /billing/cancel` - Cancel subscription
- `GET /premium/features` - Premium features page
- `GET /premium/api/data` - Premium API endpoint

## 🤝 Contributing

This is a portfolio project. Feel free to fork and customize for your own use!

## 📄 License

MIT License - feel free to use this project for learning and portfolio purposes.

## 🎓 Learning Outcomes

This project demonstrates:

- ✅ Full-stack web development with FastAPI
- ✅ Secure authentication and authorization
- ✅ Third-party API integration (Stripe)
- ✅ Webhook handling for async events
- ✅ Database modeling and relationships
- ✅ Role-based access control
- ✅ Production-ready architecture patterns

---

**Built with ❤️ using FastAPI, Stripe, and modern web technologies.**

<img width="1500" height="596" alt="image" src="https://github.com/user-attachments/assets/434366ae-a28f-4865-9311-95318f4113c0" />
<img width="1281" height="636" alt="image" src="https://github.com/user-attachments/assets/0d163a4d-f58e-4e6c-941e-8a2974972297" />
<img width="1176" height="946" alt="image" src="https://github.com/user-attachments/assets/279d6152-511a-4aec-b74b-bfe117110434" />
<img width="1360" height="776" alt="image" src="https://github.com/user-attachments/assets/aadefdea-d91c-4c01-b1c4-d06f296f1829" />
<img width="1387" height="890" alt="image" src="https://github.com/user-attachments/assets/25f38b19-7c14-41ec-aba9-91ebea406b99" />
<img width="1265" height="1122" alt="image" src="https://github.com/user-attachments/assets/cfd87181-0b66-411d-b80f-e8e21a3ca4b4" />


