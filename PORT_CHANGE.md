# Backend Port Changed from 8000 to 8001 ✅

## What Changed

The backend server port has been changed from **8000** to **8001** to avoid conflicts.

## Files Updated

### Backend Changes

1. **[backend/.env](backend/.env)** - Line 10
   ```env
   PORT=8001  # Changed from 8000
   ```

2. **[backend/start.sh](backend/start.sh)** - Lines 43-44, 50
   ```bash
   echo "🌐 Starting server on http://localhost:8001"
   echo "📚 API docs will be at http://localhost:8001/docs"
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
   ```

3. **[backend/app/main.py](backend/app/main.py)** - Lines 21-25
   ```python
   # Also updated CORS to allow frontend ports
   allow_origins=[
       "http://localhost:5173",  # Vite dev server (default)
       "http://localhost:5174",  # Vite dev server (alternate port)
       "http://localhost:3000",  # Alternative frontend port
   ]
   ```

### Frontend Changes

4. **[frontend/.env](frontend/.env)** - Line 4
   ```env
   VITE_API_URL=http://localhost:8001  # Changed from 8000
   ```

## How to Use

### Start Backend (Port 8001)

```bash
cd backend
./start.sh
```

Or manually:
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

Backend will be available at:
- **API**: http://localhost:8001
- **Docs**: http://localhost:8001/docs
- **Health**: http://localhost:8001/health

### Start Frontend (Port 5173 or 5174)

```bash
cd frontend
npm run dev
```

Frontend will be available at:
- **App**: http://localhost:5173 (or 5174 if 5173 is busy)

### Important Notes

⚠️ **After changing `.env` files, you MUST restart the servers for changes to take effect**

1. Stop both servers with `Ctrl + C`
2. Restart backend: `cd backend && ./start.sh`
3. Restart frontend: `cd frontend && npm run dev`

## Testing the Connection

### 1. Test Backend Health

```bash
curl http://localhost:8001/health
```

Expected response:
```json
{"status":"healthy"}
```

### 2. Test Backend API Docs

Open in browser: http://localhost:8001/docs

You should see the FastAPI Swagger documentation.

### 3. Test Frontend to Backend Connection

1. Open http://localhost:5173 in your browser
2. Open browser console (F12)
3. Upload a file and job description
4. Check Network tab - API calls should go to `http://localhost:8001/api/v1/upload`

## What If I Need a Different Port?

### Change Backend Port

1. Edit [backend/.env](backend/.env):
   ```env
   PORT=8002  # Or any available port
   ```

2. Edit [backend/start.sh](backend/start.sh):
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8002
   ```

3. Update frontend to use new port (see below)

### Change Frontend API URL

1. Edit [frontend/.env](frontend/.env):
   ```env
   VITE_API_URL=http://localhost:8002  # Match backend port
   ```

2. Restart frontend:
   ```bash
   cd frontend
   npm run dev
   ```

## Troubleshooting

### Error: "Address already in use"

If you see this error, port 8001 is also busy. Options:

**Option 1**: Find and stop the process using port 8001
```bash
# Find process using port 8001
lsof -ti:8001

# Kill the process
kill -9 $(lsof -ti:8001)
```

**Option 2**: Use a different port (e.g., 8002, 8003)
- Follow instructions in "What If I Need a Different Port?" above

### Error: "CORS policy blocked"

If frontend can't connect to backend:

1. Check backend CORS settings in [app/main.py](backend/app/main.py)
2. Ensure your frontend URL is in the `allow_origins` list
3. Restart backend server

### Frontend shows "Network Error"

1. Verify backend is running: `curl http://localhost:8001/health`
2. Check [frontend/.env](frontend/.env) has correct `VITE_API_URL`
3. Restart frontend with `Ctrl+C` and `npm run dev`
4. Check browser console for detailed error

## Quick Start Commands

### Start Both Servers (Two Terminals)

**Terminal 1 - Backend:**
```bash
cd /Users/manojmirji/mock-interview-app/backend
./start.sh
```

**Terminal 2 - Frontend:**
```bash
cd /Users/manojmirji/mock-interview-app/frontend
npm run dev
```

### Check If Ports Are Available

```bash
# Check if port 8001 is free
lsof -ti:8001 || echo "Port 8001 is available"

# Check if port 5173 is free
lsof -ti:5173 || echo "Port 5173 is available"
```

---

**Everything is configured! Start both servers and your app will work on the new ports.** 🚀
