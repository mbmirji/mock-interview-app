# Railway Deployment Guide for Mock Interview Backend

## Overview

This guide covers deploying the FastAPI backend to Railway.app with proper configuration.

## Prerequisites

- Railway account (free tier available)
- GitHub repository with your code
- Supabase database URL
- Google Gemini API key

## Configuration Files

The backend includes these deployment configuration files:

### 1. Procfile
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### 2. railway.json
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS",
    "buildCommand": "pip install --upgrade pip && pip install -r requirements.txt"
  },
  "deploy": {
    "startCommand": "uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 2",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10,
    "healthcheckPath": "/health",
    "healthcheckTimeout": 100
  }
}
```

### 3. nixpacks.toml
```toml
[phases.setup]
nixPkgs = ["python312", "postgresql"]

[phases.install]
cmds = ["pip install -r requirements.txt"]

[start]
cmd = "uvicorn app.main:app --host 0.0.0.0 --port $PORT"
```

### 4. runtime.txt
```
python-3.12
```

### 5. requirements.txt
Already exists with all dependencies.

## Deployment Steps

### Step 1: Prepare Your Repository

1. **Commit all changes**:
   ```bash
   cd /Users/manojmirji/mock-interview-app
   git add .
   git commit -m "Add Railway deployment configuration"
   ```

2. **Push to GitHub**:
   ```bash
   git push origin main
   ```

### Step 2: Create Railway Project

1. Go to https://railway.app
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository
5. Railway will auto-detect it's a Python app

### Step 3: Configure Root Directory

**IMPORTANT**: Since your backend is in a subdirectory, you need to configure Railway:

1. In Railway dashboard, click on your service
2. Go to **Settings** tab
3. Find **Root Directory** setting
4. Set it to: `backend`
5. Click "Save"

### Step 4: Set Environment Variables

In Railway dashboard, go to **Variables** tab and add:

```env
DATABASE_URL=postgresql://postgres.zuzxynzkasoukrjlpfks:!101Vmeady!102@aws-1-ap-south-1.pooler.supabase.com:6543/postgres

GEMINI_API_KEY=AIzaSyAepsKfQtHn5JJSo-_j81s8snnOq4wA2gw

GEMINI_MODEL=gemini-2.5-flash

ENVIRONMENT=production

PORT=8000
```

**Important Variables:**
- `DATABASE_URL` - Your Supabase connection string
- `GEMINI_API_KEY` - Your Google Gemini API key
- `GEMINI_MODEL` - Model to use (gemini-2.5-flash)
- `ENVIRONMENT` - Set to "production"
- `PORT` - Railway automatically sets this, but you can specify 8000

### Step 5: Deploy

1. Click "Deploy" or wait for auto-deploy
2. Railway will:
   - Detect Python 3.12
   - Install dependencies from requirements.txt
   - Start uvicorn server
   - Assign a public URL

### Step 6: Verify Deployment

Once deployed, Railway will provide a URL like:
```
https://your-service-name.up.railway.app
```

**Test endpoints:**
```bash
# Health check
curl https://your-service-name.up.railway.app/health

# API docs
open https://your-service-name.up.railway.app/docs

# Root endpoint
curl https://your-service-name.up.railway.app/
```

## Troubleshooting

### Issue 1: "Could not determine how to build the app"

**Cause**: Railway looking at root directory instead of backend folder

**Solution**:
1. Set **Root Directory** to `backend` in Railway Settings
2. Ensure `requirements.txt` exists in backend folder
3. Redeploy

### Issue 2: "Module not found" errors

**Cause**: Missing dependencies or wrong Python version

**Solution**:
1. Check `runtime.txt` specifies `python-3.12`
2. Verify all dependencies in `requirements.txt`
3. Check build logs for pip install errors

### Issue 3: "Port binding failed"

**Cause**: Not using Railway's $PORT variable

**Solution**:
- Ensure start command uses `--port $PORT`
- Railway automatically injects PORT variable
- Don't hardcode port 8000

### Issue 4: "Health check failed"

**Cause**: /health endpoint not responding

**Solution**:
1. Check app starts successfully in logs
2. Verify `/health` endpoint exists in `main.py`
3. Increase healthcheckTimeout in railway.json

### Issue 5: "Database connection failed"

**Cause**: Invalid DATABASE_URL or network issues

**Solution**:
1. Verify DATABASE_URL in Railway variables
2. Check Supabase database is active
3. Ensure connection string includes port 6543 (pooler)
4. Test connection string locally first

### Issue 6: "Gemini API errors"

**Cause**: Invalid API key or rate limits

**Solution**:
1. Verify GEMINI_API_KEY is correct
2. Check API key is active at https://aistudio.google.com
3. Monitor rate limits (15 requests/min on free tier)

## Monitoring

### View Logs

In Railway dashboard:
1. Click on your service
2. Go to **Deployments** tab
3. Click on latest deployment
4. View logs in real-time

**Useful log commands:**
```bash
# Using Railway CLI
railway logs

# Filter for errors
railway logs | grep ERROR
```

### Metrics

Railway provides:
- CPU usage
- Memory usage
- Network traffic
- Request count
- Response times

Access via **Metrics** tab in dashboard.

## Custom Domain (Optional)

1. Go to **Settings** tab
2. Click "Generate Domain" for free railway.app subdomain
3. Or add custom domain:
   - Click "Add Domain"
   - Enter your domain
   - Update DNS records as instructed
   - Wait for SSL certificate

## Environment-Specific Settings

### Development
```env
ENVIRONMENT=development
DEBUG=true
```

### Production
```env
ENVIRONMENT=production
DEBUG=false
```

Railway automatically uses production settings.

## Scaling

### Vertical Scaling
Railway automatically handles:
- Memory scaling
- CPU allocation
- Load balancing

### Horizontal Scaling
To add workers, update railway.json:
```json
{
  "deploy": {
    "startCommand": "uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 4"
  }
}
```

**Worker recommendations:**
- 1-2 workers: Free tier
- 2-4 workers: Hobby plan
- 4+ workers: Pro plan

## Cost Optimization

### Free Tier Limits
- $5 free credit/month
- Sleeps after 24h inactivity
- 1GB memory
- 1 vCPU

### Tips to Stay Free
1. Use single worker (`--workers 1`)
2. Enable auto-sleep
3. Use connection pooling (already configured)
4. Optimize Gemini API calls
5. Monitor usage in dashboard

## CI/CD

Railway automatically deploys on:
- Push to main branch
- Pull request merges
- Manual trigger

**Disable auto-deploy:**
1. Go to **Settings** tab
2. Uncheck "Auto-deploy"
3. Deploy manually via dashboard

## Backup & Rollback

### Create Backup
Railway keeps deployment history:
1. Go to **Deployments** tab
2. All previous deployments listed
3. Click to view details

### Rollback
1. Find working deployment
2. Click "Redeploy"
3. Service reverts to that version

## Railway CLI (Optional)

Install CLI for local testing:
```bash
# Install
npm i -g @railway/cli

# Login
railway login

# Link project
railway link

# Run locally with Railway env
railway run python -m uvicorn app.main:app --reload

# View logs
railway logs

# Open dashboard
railway open
```

## Security Best Practices

1. **Never commit secrets**
   - Use Railway environment variables
   - Don't put keys in code
   - Use .env.example for templates

2. **Update CORS**
   ```python
   # In main.py, update allow_origins
   app.add_middleware(
       CORSMiddleware,
       allow_origins=[
           "https://your-frontend.vercel.app",
           "http://localhost:5173"  # For local dev
       ],
       ...
   )
   ```

3. **Enable HTTPS only**
   - Railway provides free SSL
   - Automatically enforces HTTPS

4. **Rate limiting**
   - Implement in FastAPI
   - Or use Railway's middleware

## Testing Deployment

### Local Test with Railway Env
```bash
# Set env vars
export DATABASE_URL="your-supabase-url"
export GEMINI_API_KEY="your-api-key"

# Test server
python -m uvicorn app.main:app --reload --port 8000

# Test endpoints
curl http://localhost:8000/health
```

### Production Test
```bash
# Get your Railway URL
RAILWAY_URL="https://your-service.up.railway.app"

# Test health
curl $RAILWAY_URL/health

# Test API docs
open $RAILWAY_URL/docs

# Test upload (with files)
curl -X POST $RAILWAY_URL/api/v1/upload \
  -F "resume_file=@resume.pdf" \
  -F "job_desc_file=@job.pdf" \
  -F "additional_context=Test context"
```

## Common Railway Commands

```bash
# View service info
railway status

# View environment variables
railway variables

# Add variable
railway variables set KEY=value

# Open dashboard
railway open

# View logs
railway logs --follow

# Redeploy
railway up
```

## Checklist

- [ ] All deployment files in backend folder
- [ ] Root Directory set to "backend" in Railway
- [ ] Environment variables configured
- [ ] Database URL includes connection pooler
- [ ] CORS configured for frontend domain
- [ ] Health endpoint working
- [ ] API docs accessible
- [ ] Test upload endpoint
- [ ] Monitor logs for errors
- [ ] Set up custom domain (optional)

## Next Steps

After backend is deployed:

1. **Update Frontend**:
   - Update `VITE_API_URL` in frontend/.env
   - Use Railway URL: `https://your-service.up.railway.app`

2. **Deploy Frontend to Vercel**:
   - See FRONTEND_SETUP.md
   - Set `VITE_API_URL` environment variable

3. **Test End-to-End**:
   - Upload files from frontend
   - Verify questions generated
   - Check logs for errors

## Support

- **Railway Docs**: https://docs.railway.app
- **Railway Discord**: https://discord.gg/railway
- **Railway Status**: https://status.railway.app

---

**Your backend is ready for Railway deployment!** 🚂
