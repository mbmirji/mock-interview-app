# Quick Start Guide

Get your Mock Interview API running in 5 minutes!

---

## Local Development (3 steps)

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
```

Edit `.env`:
```bash
DATABASE_URL=postgresql://user:password@localhost:5432/mock_interview_db
OPENAI_API_KEY=sk-your-openai-key
OPENAI_MODEL=gpt-3.5-turbo
```

### 3. Run Application
```bash
# Create database tables
python create_tables.py

# Start server
uvicorn app.main:app --reload
```

Visit: **http://localhost:8000/docs** 🎉

---

## Production Deployment (Railway + Supabase)

### Prerequisites
- GitHub account
- Supabase account (free)
- Railway account (free)
- OpenAI API key

### Steps

#### 1. Set up Supabase (2 minutes)
1. Go to [supabase.com](https://supabase.com)
2. Create new project
3. Copy **Database URL** from Settings → Database

#### 2. Set up Railway (3 minutes)
1. Go to [railway.app](https://railway.app)
2. New Project → Deploy from GitHub
3. Select your repository
4. Set **Root Directory**: `backend`

#### 3. Add Environment Variables
In Railway dashboard → Variables tab:
```bash
ENVIRONMENT=production
DATABASE_URL=postgresql://postgres:password@db.xxx.supabase.co:5432/postgres
OPENAI_API_KEY=sk-your-key
OPENAI_MODEL=gpt-4
PORT=8000
```

#### 4. Deploy! 🚀
Railway auto-deploys. Get your URL from Settings → Domains.

---

## Testing Your Deployment

```bash
# Replace with your Railway URL
export API_URL=https://your-app.up.railway.app

# Test health
curl $API_URL/

# Open API docs
open $API_URL/docs
```

---

## Common Issues

### ❌ Database connection failed
**Fix**: Check DATABASE_URL format and Supabase password

### ❌ OpenAI API error
**Fix**: Verify API key and account credits

### ❌ Port binding error
**Fix**: Railway sets $PORT automatically - don't hardcode

---

## Next Steps

1. Read [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for details
2. Review API at `/docs`
3. Check [README.md](README.md) for full documentation
4. Add authentication (TODO)
5. Implement file storage (TODO)

---

## Get Help

- **Deployment Issues**: See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- **API Questions**: Check `/docs` endpoint
- **Database Schema**: See [models/__init__.py](app/models/__init__.py)

---

**You're all set! Happy coding! 🎉**
