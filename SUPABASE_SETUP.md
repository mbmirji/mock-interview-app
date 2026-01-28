# Supabase Setup Instructions

## 1. Create a Supabase Project
1. Go to [Supabase](https://supabase.com/) and create a new project.
2. Note down your project password (you will need it for the database URL).

## 2. Get Credentials
Go to **Project Settings > API** and copy:
- `Project URL` (This replaces `your-supabase-url`)
- `service_role` secret (This replaces `your-supabase-service-key`)

## 3. Configure Database
Go to **Project Settings > Database > Connection pooler** (or just use direct connection) but typically direct is fine for migration.
The Connection String looks like:
`postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres`

Update your `backend/.env` file:
```bash
DATABASE_URL="postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres"
SUPABASE_URL="https://[YOUR-PROJECT-REF].supabase.co"
SUPABASE_SERVICE_KEY="[YOUR-SERVICE-ROLE-KEY]"
SUPABASE_STORAGE_BUCKET="audio-answers"
```

## 4. Create Storage Bucket
1. Go to **Storage** in the sidebar.
2. Create a new bucket named `audio-answers`.
3. Make it **Public** (Optional but easier for reading if strictly needed, otherwise keep private and use signed URLs. The current code uses `get_public_url` so **make it Public**).
4. Add a policy if it's not public, but making it public is easiest for this demo.

## 5. Run Database Migrations
Run the following command from the `backend` directory to create all tables (`users`, `interview_sessions`, `interview_questions`, `audio_responses`):

```bash
cd backend
source venv/bin/activate  # or venv/Scripts/activate on Windows
alembic upgrade head
```

This will run the Alembic migration script (`1b2c1eb07d08_add_audio_responses.py`) which defines the schema.

## 6. Seed Data (Optional)
To create the anonymous user:
```bash
python seed.py
```
