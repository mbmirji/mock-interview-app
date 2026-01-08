# Local Development - Quick Start

## ✅ Setup Complete!

Your backend is ready to run locally with **Python 3.12** and all dependencies installed.

---

## 🎯 Just 3 Steps to Run

### 1️⃣ Get Supabase Credentials

Create a free Supabase project:
- Visit: https://supabase.com
- Create new project (takes 2 minutes)
- Get DATABASE_URL from: Settings → Database → Connection String → URI

### 2️⃣ Update `.env` File

```bash
# Edit this file
nano .env

# Update these two lines:
DATABASE_URL=<your-supabase-url>
OPENAI_API_KEY=<your-openai-key>
```

### 3️⃣ Run the Server

```bash
# Method 1: Use the start script (recommended)
./start.sh

# Method 2: Manual
source venv/bin/activate
python create_tables.py  # First time only
uvicorn app.main:app --reload
```

Visit: **http://localhost:8000/docs** 🎉

---

## 📋 What You Have

✅ **Python 3.12.12** - Installed via Homebrew
✅ **Virtual Environment** - Located in `venv/`
✅ **All Dependencies** - FastAPI, SQLAlchemy, OpenAI, etc.
✅ **Environment File** - `.env` (needs your credentials)
✅ **Start Script** - `./start.sh` for easy startup

---

## 🔑 Required Credentials

### Supabase (Free)
1. Go to https://supabase.com
2. Create new project
3. Copy DATABASE_URL from Settings → Database

### OpenAI (Paid)
1. Go to https://platform.openai.com/api-keys
2. Create new secret key
3. Copy the API key (starts with `sk-`)

---

## 📁 Important Files

| File | Purpose |
|------|---------|
| `start.sh` | One-command server start |
| `.env` | Your credentials (UPDATE THIS!) |
| `create_tables.py` | Creates DB tables on Supabase |
| `SETUP_COMPLETE.md` | Detailed setup guide |
| `LOCAL_SETUP.md` | Troubleshooting guide |

---

## 🛠️ Common Commands

```bash
# Start server
./start.sh

# Or manually:
source venv/bin/activate
uvicorn app.main:app --reload

# Create database tables (first time)
python create_tables.py

# Stop server
# Press CTRL+C

# Deactivate virtual environment
deactivate
```

---

## 🐛 Quick Troubleshooting

### Can't start server?
```bash
# Make sure you're in the backend directory
cd /Users/manojmirji/mock-interview-app/backend

# Activate virtual environment
source venv/bin/activate

# Check Python version
python --version  # Should be 3.12.x
```

### Database connection error?
- Check DATABASE_URL in `.env`
- Verify Supabase project is active
- Run `python create_tables.py` if tables don't exist

### OpenAI API error?
- Verify OPENAI_API_KEY in `.env`
- Check account has credits
- Try `gpt-3.5-turbo` instead of `gpt-4`

---

## 📚 Documentation

- **Setup Guide**: [SETUP_COMPLETE.md](SETUP_COMPLETE.md)
- **Local Setup**: [LOCAL_SETUP.md](LOCAL_SETUP.md)
- **Deployment**: [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- **API Docs**: http://localhost:8000/docs (when running)

---

## 🚀 Next Steps

1. Update `.env` with your credentials
2. Run `./start.sh`
3. Visit http://localhost:8000/docs
4. Test the API with sample PDFs
5. When ready, deploy to Railway!

---

**Need help?** Check [SETUP_COMPLETE.md](SETUP_COMPLETE.md) for detailed instructions.
