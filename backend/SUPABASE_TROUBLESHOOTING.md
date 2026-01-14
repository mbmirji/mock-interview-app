# Supabase Connection Troubleshooting

## Current Error
```
psycopg2.OperationalError: could not translate host name "db.zuzxynzkasoukrjlpfks.supabase.co" to address: nodename nor servname provided, or not known
```

## What This Means
The hostname in your DATABASE_URL cannot be resolved via DNS. This typically indicates:
1. The Supabase project is paused or not initialized
2. The connection string has an incorrect project reference
3. There's a typo in the connection string

## Solution Steps

### Step 1: Verify Supabase Project Status
1. Go to https://supabase.com/dashboard
2. Log in with your account
3. Look for your project in the list
4. Check if it shows "Paused" or "Inactive"
5. If paused, click "Restore" to reactivate it

### Step 2: Get the Correct Connection String

#### Option A: Connection Pooling (Recommended)
1. In Supabase dashboard, select your project
2. Go to **Settings → Database**
3. Scroll to **Connection String** section
4. Select **Connection Pooling** tab (not Transaction or Session)
5. Mode: **Transaction** or **Session** (Transaction is recommended)
6. Copy the URI - it should look like:
   ```
   postgresql://postgres.[PROJECT-REF]:[PASSWORD]@aws-0-[region].pooler.supabase.com:6543/postgres
   ```
7. Replace `[PASSWORD]` with your actual database password

#### Option B: Direct Connection
1. In the same section, select **Direct Connection** tab
2. Copy the URI - it should look like:
   ```
   postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
   ```
3. Replace `[PASSWORD]` with your actual database password

### Step 3: Update Your .env File

Open `.env` and update the DATABASE_URL:

```bash
# Old (not working):
DATABASE_URL=postgresql://postgres:!100Vmeady!101@db.zuzxynzkasoukrjlpfks.supabase.co:5432/postgres

# New (get from Supabase dashboard):
DATABASE_URL=postgresql://postgres.[PROJECT-REF]:[YOUR-PASSWORD]@aws-0-us-east-1.pooler.supabase.com:6543/postgres
```

### Step 4: Test the Connection

```bash
# Activate virtual environment
source venv/bin/activate

# Try creating tables again
python create_tables.py
```

## Alternative: Create Tables via Supabase SQL Editor

If you prefer to create tables directly through Supabase:

1. Go to **SQL Editor** in Supabase dashboard
2. Click **New Query**
3. Copy the SQL schema from `app/models/__init__.py`
4. Paste and run in the SQL editor

### SQL Schema to Run:

```sql
-- Users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    full_name VARCHAR(255),
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE INDEX IF NOT EXISTS ix_users_email ON users(email);
CREATE INDEX IF NOT EXISTS ix_users_username ON users(username);

-- Interview sessions table
CREATE TABLE IF NOT EXISTS interview_sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    resume_filename VARCHAR(500),
    resume_content TEXT,
    job_description TEXT NOT NULL,
    status VARCHAR(50) DEFAULT 'created' NOT NULL,
    total_questions INTEGER DEFAULT 0,
    answered_questions INTEGER DEFAULT 0,
    average_score FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    completed_at TIMESTAMP
);

CREATE INDEX IF NOT EXISTS ix_interview_sessions_user_id ON interview_sessions(user_id);
CREATE INDEX IF NOT EXISTS ix_interview_sessions_status ON interview_sessions(status);

-- Interview questions table
CREATE TABLE IF NOT EXISTS interview_questions (
    id SERIAL PRIMARY KEY,
    session_id INTEGER NOT NULL REFERENCES interview_sessions(id) ON DELETE CASCADE,
    question_text TEXT NOT NULL,
    reference_answer TEXT,
    user_answer TEXT,
    score FLOAT,
    feedback TEXT,
    question_order INTEGER NOT NULL,
    is_answered BOOLEAN DEFAULT FALSE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE INDEX IF NOT EXISTS ix_interview_questions_session_id ON interview_questions(session_id);
CREATE INDEX IF NOT EXISTS ix_interview_questions_is_answered ON interview_questions(is_answered);
```

## Verification

After updating the DATABASE_URL and running create_tables.py successfully, you should see:
```
Creating database tables...
✓ All tables created successfully!
```

## Common Issues

### Issue: "SSL connection required"
**Solution**: Your connection string needs `?sslmode=require` at the end:
```
DATABASE_URL=postgresql://...postgres?sslmode=require
```

### Issue: "Authentication failed"
**Solution**:
- Verify your database password is correct
- In Supabase dashboard, go to Settings → Database → Reset Database Password

### Issue: "Connection timeout"
**Solution**:
- Check your firewall isn't blocking outbound connections to Supabase
- Try using the connection pooler (port 6543) instead of direct connection (port 5432)

## Need More Help?

Check the official Supabase documentation:
- Connection Strings: https://supabase.com/docs/guides/database/connecting-to-postgres
- Connection Pooling: https://supabase.com/docs/guides/database/connecting-to-postgres#connection-pooler

---

**Next Step**: Update your DATABASE_URL in `.env` with the correct connection string from your Supabase dashboard.
