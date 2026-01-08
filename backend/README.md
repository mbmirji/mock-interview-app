# Mock Interview API - Backend

FastAPI backend for the Mock Interview application with Supabase PostgreSQL and OpenAI integration.

---

## 🚀 Quick Start

### Local Development

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up environment
cp .env.example .env
# Edit .env with your configuration

# 3. Create database tables
python create_tables.py

# 4. Run development server
uvicorn app.main:app --reload
```

Visit: http://localhost:8000/docs

---

## 📦 Tech Stack

- **Framework**: FastAPI 0.109.0
- **Database**: PostgreSQL (Supabase)
- **ORM**: SQLAlchemy 2.0
- **LLM**: OpenAI GPT-4 / GPT-3.5 Turbo
- **Deployment**: Railway
- **Document Processing**: PyPDF2, python-docx, pdfplumber

---

## 🗂️ Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry
│   ├── config.py            # Configuration settings
│   ├── api/
│   │   └── endpoints/
│   │       └── __init__.py  # API endpoints
│   ├── models/
│   │   └── __init__.py      # SQLAlchemy models
│   ├── schemas/
│   │   └── __init__.py      # Pydantic schemas
│   ├── services/
│   │   └── __init__.py      # LLM service
│   └── database/
│       └── __init__.py      # Database configuration
├── .env.example             # Environment template
├── .env.development         # Dev environment
├── .env.production          # Prod environment
├── requirements.txt         # Python dependencies
├── Procfile                 # Railway deployment
├── railway.json             # Railway configuration
├── create_tables.py         # Database initialization
└── DEPLOYMENT_GUIDE.md      # Deployment instructions
```

---

## 🗄️ Database Schema

### Users
- User authentication and profiles
- Relationships: One-to-many with interview sessions

### Interview Sessions
- Mock interview attempts
- Stores resume and job description
- Tracks session status and statistics

### Interview Questions
- Individual Q&A within sessions
- LLM-generated questions and answers
- User responses and scoring

See [models/__init__.py](app/models/__init__.py) for full schema.

---

## 🔧 Configuration

### Environment Variables

```bash
# Application
ENVIRONMENT=development  # development, staging, production
DEBUG=true
PORT=8000

# Supabase Database
DATABASE_URL=postgresql://postgres:password@host:5432/postgres

# OpenAI
OPENAI_API_KEY=sk-your-api-key
OPENAI_MODEL=gpt-4  # or gpt-3.5-turbo

# File Upload
MAX_FILE_SIZE_MB=10
```

### Configuration Files
- `.env` - Your local config (git-ignored)
- `.env.example` - Template with all options
- `.env.development` - Development defaults
- `.env.production` - Production settings

---

## 📡 API Endpoints

### Upload Documents
```http
POST /api/v1/upload
Content-Type: multipart/form-data

Files:
- resume: PDF/DOC/DOCX
- job_description: PDF/DOC/DOCX

Response: Interview session with generated questions
```

### Get All Interviews
```http
GET /api/v1/interviews
Response: List of all interview sessions
```

### Get Interview by ID
```http
GET /api/v1/interviews/{id}
Response: Specific interview session
```

### Get Interview Questions
```http
GET /api/v1/interviews/{id}/questions
Response: Questions and answers for session
```

See interactive API docs at `/docs` when running.

---

## 🚢 Deployment

### Railway + Supabase

1. **Set up Supabase**:
   - Create project at [supabase.com](https://supabase.com)
   - Get DATABASE_URL from Settings → Database

2. **Deploy to Railway**:
   - Push code to GitHub
   - Import repo to [railway.app](https://railway.app)
   - Add environment variables
   - Deploy!

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions.

---

## 🧪 Testing

### Test Database Connection
```bash
python -c "from app.database import engine; engine.connect(); print('✓ Connected')"
```

### Test OpenAI Integration
```bash
python -c "from app.services import get_llm_service; svc = get_llm_service(); print('✓ LLM Ready')"
```

### Run API Tests
```bash
# Install test dependencies
pip install pytest httpx

# Run tests
pytest
```

---

## 📝 File Upload Validation

Supported formats:
- ✅ PDF (`.pdf`)
- ✅ Word 2007+ (`.docx`)
- ✅ Word 97-2003 (`.doc`)

Max file size: 10 MB (configurable)

Validation at [endpoints/__init__.py:12](app/api/endpoints/__init__.py#L12)

---

## 🔐 Security

- ✅ File type validation
- ✅ File size limits
- ✅ Environment-based configuration
- ✅ SSL for database connections
- ⚠️ TODO: Add authentication
- ⚠️ TODO: Add rate limiting
- ⚠️ TODO: Add CORS configuration

---

## 💰 Cost Estimates

### Development (Local)
- Free with local PostgreSQL

### Production (Railway + Supabase)
- **Supabase Free**: $0/month (500 MB DB)
- **Railway Free**: $0-5/month ($5 credit)
- **OpenAI**: $5-50/month (usage-based)
- **Total**: ~$5-55/month

---

## 🛠️ Development

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Database Migrations
```bash
# Create tables
python create_tables.py

# TODO: Add Alembic for migrations
# alembic init alembic
# alembic revision --autogenerate -m "Initial"
# alembic upgrade head
```

### Code Style
```bash
# Format code
black app/

# Lint
flake8 app/
```

---

## 🐛 Troubleshooting

### Database Connection Issues
```bash
# Check connection string format
echo $DATABASE_URL

# Test connection
python -c "from app.database import engine; engine.connect()"
```

### OpenAI API Errors
- Verify API key is valid
- Check account has credits
- Try `gpt-3.5-turbo` instead of `gpt-4`

### Railway Deployment
- Ensure `Procfile` exists
- Check `railway.json` configuration
- View logs in Railway dashboard

---

## 📚 Resources

- **FastAPI Docs**: https://fastapi.tiangolo.com
- **SQLAlchemy Docs**: https://docs.sqlalchemy.org
- **Supabase Docs**: https://supabase.com/docs
- **Railway Docs**: https://docs.railway.app
- **OpenAI API**: https://platform.openai.com/docs

---

## 📄 License

MIT License - see LICENSE file for details

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📧 Support

For issues and questions:
- Open an issue on GitHub
- Check [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- Review API docs at `/docs`

---

**Built with ❤️ using FastAPI, Supabase, and OpenAI**
