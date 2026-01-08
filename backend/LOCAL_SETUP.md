# Local Backend Setup Guide

Quick guide to get your backend running locally.

## Prerequisites

- Python 3.11 or 3.12 (3.13 has compatibility issues)
- PostgreSQL (optional - can use Supabase directly)
- OpenAI API Key

---

## Option 1: Use Supabase Directly (Recommended)

Skip local PostgreSQL installation and connect directly to Supabase!

### Steps:

1. **Create Supabase Project**
   - Go to [supabase.com](https://supabase.com)
   - Create new project
   - Get DATABASE_URL from Settings → Database

2. **Set up Python Environment**
   ```bash
   cd backend

   # Create virtual environment with Python 3.12
   python3.12 -m venv venv
   # Or if you only have Python 3.13:
   python3 -m venv venv

   # Activate virtual environment
   source venv/bin/activate

   # Upgrade pip
   pip install --upgrade pip
   ```

3. **Install Dependencies**
   ```bash
   # Try installing requirements
   pip install -r requirements.txt

   # If psycopg2-binary fails with Python 3.13, try:
   pip install psycopg2-binary --no-binary psycopg2-binary
   # Or use psycopg (newer version):
   pip install "psycopg[binary,pool]"
   ```

4. **Configure Environment**
   ```bash
   cp .env.example .env
   ```

   Edit `.env`:
   ```bash
   # Supabase Database
   DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres

   # OpenAI
   OPENAI_API_KEY=sk-your-openai-api-key
   OPENAI_MODEL=gpt-3.5-turbo  # Cheaper for development

   # App
   ENVIRONMENT=development
   DEBUG=true
   PORT=8000
   ```

5. **Create Database Tables**
   ```bash
   python create_tables.py
   ```

6. **Run Server**
   ```bash
   uvicorn app.main:app --reload
   ```

7. **Test API**
   Visit: http://localhost:8000/docs

---

## Option 2: Local PostgreSQL

If you want to run PostgreSQL locally:

### 1. Install PostgreSQL
```bash
brew install postgresql@15
```

### 2. Start PostgreSQL
```bash
brew services start postgresql@15
```

### 3. Create Database
```bash
/opt/homebrew/opt/postgresql@15/bin/createdb mock_interview_db
```

### 4. Update .env
```bash
DATABASE_URL=postgresql://$(whoami)@localhost:5432/mock_interview_db
OPENAI_API_KEY=sk-your-key
OPENAI_MODEL=gpt-3.5-turbo
```

### 5. Follow steps 2-7 from Option 1

---

## Troubleshooting

### Issue: Python 3.13 Compatibility

Some packages don't support Python 3.13 yet. Solutions:

**Solution 1: Use Python 3.12**
```bash
brew install python@3.12
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Solution 2: Use psycopg instead of psycopg2-binary**

Edit `requirements.txt`, replace:
```
psycopg2-binary==2.9.9
```

With:
```
psycopg[binary]==3.1.18
```

Then update `app/database/__init__.py` if needed.

### Issue: psycopg2-binary build fails

```bash
# Install PostgreSQL first
brew install postgresql@15

# Add to PATH
export PATH="/opt/homebrew/opt/postgresql@15/bin:$PATH"

# Try again
pip install psycopg2-binary
```

### Issue: OpenAI API Error

- Verify API key is correct
- Check you have credits in your OpenAI account
- Try `gpt-3.5-turbo` instead of `gpt-4`

### Issue: Database Connection Failed

**For Supabase:**
- Check DATABASE_URL format
- Verify password doesn't need URL encoding
- Ensure project isn't paused (free tier auto-pauses)

**For Local PostgreSQL:**
- Ensure PostgreSQL is running: `brew services list`
- Check database exists: `/opt/homebrew/opt/postgresql@15/bin/psql -l`

---

## Quick Commands

```bash
# Activate venv
source venv/bin/activate

# Run server
uvicorn app.main:app --reload

# Run with specific port
uvicorn app.main:app --reload --port 8080

# Create tables
python create_tables.py

# Deactivate venv
deactivate
```

---

## Next Steps

1. Get API working locally
2. Test with PDF/Word uploads
3. Deploy to Railway when ready

For deployment: See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
