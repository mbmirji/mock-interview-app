# ✅ Backend Setup Complete!

Your backend is ready to run! Here's what's been set up:

## What's Installed

✅ Python 3.12.12
✅ Virtual environment (`venv/`)
✅ All Python dependencies
✅ Environment file (`.env`)
✅ PostgreSQL 15 (available if needed)

---

## Next Steps

### 1. Set Up Supabase Database

You need a Supabase database to run the application.

**Quick Setup** (5 minutes):

1. Go to [supabase.com](https://supabase.com)
2. Click "Start your project" → Sign in with GitHub
3. Click "New Project"
4. Fill in:
   - **Name**: `mock-interview-db`
   - **Database Password**: Create a strong password (save it!)
   - **Region**: Choose closest to you (e.g., US East)
5. Click "Create new project" (wait ~2 minutes)

### 2. Get Your Database Connection String

1. In Supabase dashboard → **Settings** (gear icon) → **Database**
2. Scroll to **Connection String** section
3. Select **URI** tab
4. Copy the connection string (looks like this):
   ```
   postgresql://postgres.[PROJECT-ID]:[YOUR-PASSWORD]@aws-0-us-east-1.pooler.supabase.com:6543/postgres
   ```

### 3. Update Your `.env` File

Open `/Users/manojmirji/mock-interview-app/backend/.env` and update:

```bash
# Replace this line:
DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres

# With your actual Supabase connection string from step 2
DATABASE_URL=postgresql://postgres.xxxxxxxxxxxx:[password]@aws-0-us-east-1.pooler.supabase.com:6543/postgres

# Also add your OpenAI API key:
OPENAI_API_KEY=sk-your-actual-openai-api-key
```

**Get OpenAI API Key**:
- Go to [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
- Create new secret key
- Copy and paste into `.env`

### 4. Create Database Tables

```bash
cd /Users/manojmirji/mock-interview-app/backend
source venv/bin/activate
python create_tables.py
```

You should see:
```
Creating database tables...
✓ All tables created successfully!

Created tables:
  - users
  - interview_sessions
  - interview_questions
  - interviews (legacy)
```

### 5. Start the Server

```bash
uvicorn app.main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### 6. Test the API

Open your browser to: **http://localhost:8000/docs**

You'll see the interactive API documentation (Swagger UI) where you can:
- Upload PDF/Word files
- Test the interview question generation
- View all endpoints

---

## Quick Reference Commands

```bash
# Activate virtual environment
cd /Users/manojmirji/mock-interview-app/backend
source venv/bin/activate

# Run server
uvicorn app.main:app --reload

# Run server on different port
uvicorn app.main:app --reload --port 8080

# Create/update database tables
python create_tables.py

# Deactivate virtual environment
deactivate
```

---

## File Structure

```
backend/
├── venv/                    ✅ Virtual environment (Python 3.12)
├── app/
│   ├── main.py             → FastAPI application
│   ├── config.py           → Settings (reads from .env)
│   ├── models/             → Database models
│   ├── api/endpoints/      → API routes
│   ├── services/           → LLM service (OpenAI)
│   └── database/           → Database connection
├── .env                    ⚠️  UPDATE WITH YOUR KEYS
├── requirements.txt        ✅ All dependencies installed
├── create_tables.py        → Run this to create DB tables
└── Procfile                → For Railway deployment
```

---

## Troubleshooting

### Can't connect to database

**Issue**: `OperationalError: connection to server failed`

**Solutions**:
1. Verify DATABASE_URL in `.env` is correct
2. Check Supabase project is not paused
3. Ensure password in URL doesn't need encoding

### OpenAI API errors

**Issue**: `AuthenticationError` or `RateLimitError`

**Solutions**:
1. Verify OPENAI_API_KEY in `.env`
2. Check account has credits
3. Use `gpt-3.5-turbo` instead of `gpt-4` (cheaper)

### Port already in use

**Issue**: `Address already in use`

**Solution**:
```bash
# Use different port
uvicorn app.main:app --reload --port 8080

# Or kill process using port 8000
lsof -ti:8000 | xargs kill -9
```

---

## What's Next?

1. **Test locally**: Upload some PDFs and test the API
2. **Check tables**: Verify tables created in Supabase dashboard
3. **Deploy**: When ready, follow [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

---

## Support

- **Local Setup Issues**: See [LOCAL_SETUP.md](LOCAL_SETUP.md)
- **Deployment**: See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- **API Documentation**: http://localhost:8000/docs (when running)

---

**Your backend is ready! 🚀**

Just update `.env` with your Supabase and OpenAI credentials, create the tables, and start coding!
