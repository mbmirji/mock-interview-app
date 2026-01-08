# Deployment Guide - Railway + Supabase

This guide walks you through deploying your Mock Interview API to Railway with Supabase PostgreSQL.

---

## Table of Contents
1. [Supabase PostgreSQL Setup](#1-supabase-postgresql-setup)
2. [Railway Deployment](#2-railway-deployment)
3. [Environment Variables](#3-environment-variables)
4. [Database Migration](#4-database-migration)
5. [Testing](#5-testing)
6. [Troubleshooting](#6-troubleshooting)

---

## 1. Supabase PostgreSQL Setup

### Step 1: Create Supabase Account

1. Go to [supabase.com](https://supabase.com)
2. Click "Start your project"
3. Sign up with GitHub (recommended) or email

### Step 2: Create New Project

1. Click "New Project"
2. Fill in project details:
   - **Name**: `mock-interview-db` (or your choice)
   - **Database Password**: Generate a strong password (save it!)
   - **Region**: Choose closest to your users (e.g., `US East`)
   - **Pricing Plan**: Free tier (500 MB database, 500 MB storage)

3. Click "Create new project"
4. Wait 2-3 minutes for project to be provisioned

### Step 3: Get Database Connection String

1. Go to **Settings** (gear icon) → **Database**
2. Scroll to **Connection String** section
3. Select **URI** tab
4. Copy the connection string:
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
   ```
5. Replace `[YOUR-PASSWORD]` with your actual database password

### Step 4: Configure Database (Optional)

**Connection Pooling** (recommended for production):
1. Go to **Settings** → **Database** → **Connection Pooling**
2. Enable connection pooling
3. Use the pooled connection string for Railway:
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.[PROJECT-REF].supabase.co:6543/postgres?pgbouncer=true
   ```

**Note**: Port `6543` is for pooled connections, `5432` is direct

---

## 2. Railway Deployment

### Step 1: Create Railway Account

1. Go to [railway.app](https://railway.app)
2. Click "Login" → "Login with GitHub"
3. Authorize Railway to access your GitHub

### Step 2: Create New Project

1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Connect your GitHub account if not already connected
4. Select your `mock-interview-app` repository
5. Railway will detect it as a Python project

### Step 3: Configure Build Settings

1. In Railway dashboard, click on your service
2. Go to **Settings** tab
3. Configure:
   - **Root Directory**: `backend` (important!)
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Step 4: Add Procfile (Alternative)

Create a `Procfile` in your `backend/` directory:

```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Railway will automatically detect and use this.

---

## 3. Environment Variables

### Step 1: Add Variables in Railway

1. In Railway dashboard, go to **Variables** tab
2. Add the following variables:

```bash
# Application
ENVIRONMENT=production
DEBUG=false
PORT=8000

# Supabase Database
DATABASE_URL=postgresql://postgres:[password]@db.[project-ref].supabase.co:5432/postgres

# OpenAI
OPENAI_API_KEY=sk-your-production-key
OPENAI_MODEL=gpt-4

# File Upload
MAX_FILE_SIZE_MB=10
```

### Step 2: Get OpenAI API Key

1. Go to [platform.openai.com](https://platform.openai.com)
2. Sign in or create account
3. Go to **API Keys** → **Create new secret key**
4. Copy the key (starts with `sk-`)
5. Paste into Railway `OPENAI_API_KEY` variable

### Railway Environment Variables Tips

- Railway automatically provides `$PORT` - don't hardcode port 8000
- Use Railway's **Secret Management** for sensitive data
- Variables are encrypted at rest

---

## 4. Database Migration

### Option 1: Run Migration from Railway (Recommended)

1. **Add migration command to Railway**:
   - Go to Railway → **Settings** → **Deploy**
   - Add a **Deploy Command**:
     ```bash
     python create_tables.py && uvicorn app.main:app --host 0.0.0.0 --port $PORT
     ```

2. **Or use Railway CLI** (one-time):
   ```bash
   # Install Railway CLI
   npm i -g @railway/cli

   # Login
   railway login

   # Link to your project
   railway link

   # Run migration
   railway run python backend/create_tables.py
   ```

### Option 2: Run Migration Locally

1. **Update your local `.env`** with Supabase connection string
2. **Run migration**:
   ```bash
   cd backend
   python create_tables.py
   ```

### Verify Tables Created

1. Go to Supabase dashboard
2. Click **Table Editor** (left sidebar)
3. You should see:
   - `users`
   - `interview_sessions`
   - `interview_questions`
   - `interviews` (legacy)

---

## 5. Testing

### Test Locally First

```bash
# 1. Install dependencies
cd backend
pip install -r requirements.txt

# 2. Set up local .env with Supabase
cp .env.example .env
# Edit .env with your Supabase DATABASE_URL

# 3. Create tables
python create_tables.py

# 4. Run locally
uvicorn app.main:app --reload

# 5. Test API
curl http://localhost:8000/docs
```

### Test Railway Deployment

1. **Get your Railway URL**:
   - Go to Railway dashboard → **Settings** → **Domains**
   - You'll see a URL like: `https://your-app.up.railway.app`
   - Or add a custom domain

2. **Test API endpoints**:
   ```bash
   # Health check
   curl https://your-app.up.railway.app/

   # API docs
   open https://your-app.up.railway.app/docs
   ```

3. **Test upload endpoint**:
   - Go to `https://your-app.up.railway.app/docs`
   - Try the `/api/v1/upload` endpoint
   - Upload test PDF/Word files

---

## 6. Troubleshooting

### Common Issues

#### ❌ Build Failed
**Problem**: Railway can't find `requirements.txt`
**Solution**: Set **Root Directory** to `backend` in Railway settings

#### ❌ Database Connection Failed
**Problem**: Can't connect to Supabase
**Solutions**:
- Verify DATABASE_URL is correct
- Check password doesn't have special characters needing URL encoding
- Use connection pooling URL (port 6543) for better performance
- Ensure Supabase project is not paused (free tier auto-pauses after inactivity)

#### ❌ Port Binding Error
**Problem**: `Error binding to port`
**Solution**: Use `--port $PORT` not hardcoded port:
```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

#### ❌ OpenAI API Error
**Problem**: OpenAI rate limit or invalid key
**Solutions**:
- Verify API key is correct
- Check OpenAI account has credits
- Use `gpt-3.5-turbo` instead of `gpt-4` to save costs

#### ❌ File Upload Fails
**Problem**: PDF/Word files not uploading
**Solutions**:
- Check file size limits (default 10MB)
- Verify `python-multipart` is installed
- Check file type validation logic

### Viewing Logs

**Railway Logs**:
1. Go to Railway dashboard
2. Click **Deployments** tab
3. Click on latest deployment
4. View build and runtime logs

**Supabase Logs**:
1. Go to Supabase dashboard
2. Click **Logs** (left sidebar)
3. View database queries and errors

### Performance Monitoring

**Railway**:
- View metrics: CPU, Memory, Network in **Metrics** tab
- Set up alerts for high usage

**Supabase**:
- Monitor database size in **Database** settings
- Check connection pool usage
- Free tier: 500 MB limit

---

## Cost Estimates

### Supabase Free Tier
- ✅ 500 MB database
- ✅ 1 GB file storage
- ✅ 50,000 monthly active users
- ✅ 500 MB egress
- **Cost**: $0/month

### Railway Free Tier
- ✅ $5 monthly credit
- ✅ 500 hours/month execution
- ✅ 100 GB outbound network
- **Cost**: ~$0-5/month (depends on usage)

### OpenAI API
- GPT-4: $0.03 per 1K tokens (input), $0.06 per 1K tokens (output)
- GPT-3.5 Turbo: $0.0015 per 1K tokens (input), $0.002 per 1K tokens (output)
- **Estimated**: $5-50/month depending on usage

**Total**: ~$5-55/month for small to medium usage

---

## Production Best Practices

### Security
1. ✅ Use environment variables, never hardcode secrets
2. ✅ Enable CORS restrictions in FastAPI
3. ✅ Use HTTPS only (Railway provides this automatically)
4. ✅ Implement rate limiting
5. ✅ Add authentication to endpoints

### Database
1. ✅ Use connection pooling (Supabase port 6543)
2. ✅ Regular backups (Supabase does this automatically)
3. ✅ Monitor database size
4. ✅ Add indexes for frequently queried fields

### Monitoring
1. ✅ Set up Railway usage alerts
2. ✅ Monitor OpenAI API costs
3. ✅ Track error rates in logs
4. ✅ Use Supabase analytics

### Scaling
When you outgrow free tier:
- **Railway**: Upgrade to Hobby ($5/month) or Pro ($20/month)
- **Supabase**: Upgrade to Pro ($25/month) for 8 GB database
- **OpenAI**: Add billing limits and alerts

---

## Next Steps

1. ✅ Set up custom domain in Railway
2. ✅ Implement user authentication
3. ✅ Add file storage (Supabase Storage)
4. ✅ Set up CI/CD with GitHub Actions
5. ✅ Add monitoring and alerting
6. ✅ Implement caching for LLM responses

---

## Useful Links

- **Railway Docs**: https://docs.railway.app
- **Supabase Docs**: https://supabase.com/docs
- **FastAPI Deployment**: https://fastapi.tiangolo.com/deployment/
- **OpenAI API Docs**: https://platform.openai.com/docs

---

## Support

- Railway Discord: https://discord.gg/railway
- Supabase Discord: https://discord.supabase.com
- OpenAI Community: https://community.openai.com

---

**Happy Deploying! 🚀**
