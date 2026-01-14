# Frontend Setup Complete! ✅

Your React + TypeScript + Vite + Tailwind CSS frontend is ready!

## What Was Built

### Technology Stack
- ⚡ **Vite** - Lightning-fast dev server and build tool
- ⚛️ **React 18** - Modern React with hooks
- 📘 **TypeScript** - Full type safety
- 🎨 **Tailwind CSS** - Utility-first styling
- 📡 **Axios** - HTTP client for API calls

### Features Implemented

#### 1. File Upload Component
- Drag-and-drop file upload
- File type validation (PDF, DOC, DOCX only)
- File size validation (max 10MB)
- Visual feedback for drag state
- Error handling
- File preview with size display

#### 2. Question List Component
- Displays generated questions
- Shows reference answers
- Numbered question list
- Clean, card-based UI
- Responsive design

#### 3. Upload Page
- Resume file upload
- Job description textarea
- Form validation
- Loading states
- Error messages
- Success feedback
- Question display after generation

### Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── FileUpload.tsx       # Drag-drop file upload
│   │   └── QuestionList.tsx     # Display questions
│   ├── pages/
│   │   └── UploadPage.tsx       # Main upload page
│   ├── services/
│   │   └── api.ts               # Backend API calls
│   ├── types/
│   │   └── index.ts             # TypeScript interfaces
│   ├── App.tsx                  # Root component
│   ├── main.tsx                 # Entry point
│   └── index.css                # Tailwind imports
├── .env                         # Environment variables
├── vercel.json                  # Vercel deployment config
├── tailwind.config.js           # Tailwind configuration
├── package.json                 # Dependencies
└── README.md                    # Documentation
```

## Getting Started

### Step 1: Start the Frontend

```bash
# Navigate to frontend directory
cd frontend

# Start development server
npm run dev

# Or use the start script
./start.sh
```

The frontend will be available at: **http://localhost:5173**

### Step 2: Start the Backend

In a separate terminal:

```bash
# Navigate to backend directory
cd backend

# Start backend server
./start.sh

# Or manually
source venv/bin/activate
uvicorn app.main:app --reload
```

The backend will be available at: **http://localhost:8000**

### Step 3: Test the Application

1. Open http://localhost:5173 in your browser
2. Upload a resume file (PDF, DOC, or DOCX)
3. Paste a job description
4. Click "Generate Interview Questions"
5. View the generated questions!

## How It Works

### Upload Flow

1. **User uploads resume** → File validated on client-side
2. **User enters job description** → Form validates both inputs
3. **Click "Generate Questions"** → Loading state shown
4. **Frontend sends to backend** → POST `/api/v1/upload` with FormData
5. **Backend processes** → Extracts resume text, calls Gemini API
6. **Questions generated** → Backend returns session + questions
7. **Frontend displays** → Questions shown in cards

### API Integration

The frontend uses Axios to communicate with your FastAPI backend:

```typescript
// Upload resume and job description
const response = await uploadResumeAndJobDescription(file, jobDescription);

// Response contains:
{
  session_id: 123,
  questions: [
    {
      id: 1,
      question_text: "...",
      reference_answer: "...",
      question_order: 1
    }
  ],
  message: "Questions generated successfully"
}
```

## Environment Configuration

### Development (.env)
```env
VITE_API_URL=http://localhost:8000
```

### Production (Vercel)
```env
VITE_API_URL=https://your-backend.railway.app
```

## Deployment to Vercel

### Quick Deploy

1. **Initialize Git** (if not already):
   ```bash
   cd /Users/manojmirji/mock-interview-app
   git init
   git add .
   git commit -m "Initial commit: Mock Interview App"
   ```

2. **Push to GitHub**:
   - Create a new repository on GitHub
   - Follow GitHub's instructions to push your code

3. **Deploy to Vercel**:
   - Go to https://vercel.com
   - Click "New Project"
   - Import your GitHub repository
   - Configure:
     - **Framework Preset**: Vite
     - **Root Directory**: `frontend`
     - **Build Command**: `npm run build`
     - **Output Directory**: `dist`
   - Add Environment Variable:
     - Key: `VITE_API_URL`
     - Value: Your Railway backend URL (e.g., `https://mock-interview-backend.railway.app`)
   - Click "Deploy"

4. **Update Backend CORS**:
   After deployment, update your backend's [main.py](backend/app/main.py) to allow your Vercel domain:

   ```python
   app.add_middleware(
       CORSMiddleware,
       allow_origins=[
           "http://localhost:5173",                    # Local dev
           "https://your-app.vercel.app",             # Production
       ],
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

## Testing the Frontend

### Manual Testing Checklist

- [ ] File upload accepts PDF files
- [ ] File upload accepts DOC/DOCX files
- [ ] File upload rejects other file types (txt, jpg, etc.)
- [ ] File upload rejects files > 10MB
- [ ] Drag and drop works
- [ ] Job description is required
- [ ] Loading spinner shows during API call
- [ ] Error messages display correctly
- [ ] Questions display after successful upload
- [ ] Can start new session after viewing questions

### Test Data

Use these for testing:
- **Resume**: Any PDF resume file
- **Job Description**:
  ```
  We are looking for a Senior Software Engineer with 5+ years of experience
  in Python, FastAPI, and React. Must have experience with PostgreSQL,
  AWS/GCP, Docker, and microservices architecture.
  ```

## File Validation

### Client-Side Validation
- File type: `.pdf`, `.doc`, `.docx` only
- File size: Maximum 10MB
- User-friendly error messages

### Server-Side Validation
Your backend also validates:
- File type verification
- Content extraction
- Request validation

## Customization

### Styling

Tailwind classes are used throughout. To customize:

1. **Colors**: Edit [tailwind.config.js](frontend/tailwind.config.js)
2. **Components**: Modify files in [src/components/](frontend/src/components/)
3. **Layout**: Update [src/pages/UploadPage.tsx](frontend/src/pages/UploadPage.tsx)

### Configuration

1. **API URL**: Change in [.env](frontend/.env)
2. **Max file size**: Update in [FileUpload.tsx:48](frontend/src/components/FileUpload.tsx#L48)
3. **Allowed extensions**: Update in [FileUpload.tsx:47](frontend/src/components/FileUpload.tsx#L47)

## Troubleshooting

### Issue: "Failed to upload" error

**Cause**: Backend not running or CORS misconfigured

**Solution**:
1. Check backend is running: `curl http://localhost:8000/health`
2. Check browser console for CORS errors
3. Verify `VITE_API_URL` in `.env`

### Issue: File upload validation not working

**Cause**: File extension check failing

**Solution**:
- Check file has proper extension
- Ensure file size < 10MB
- Check browser console for errors

### Issue: Tailwind styles not applying

**Cause**: Tailwind not properly configured

**Solution**:
```bash
# Rebuild node_modules
rm -rf node_modules package-lock.json
npm install

# Clear Vite cache
rm -rf node_modules/.vite
npm run dev
```

## Next Steps

### Immediate
1. ✅ Test the application end-to-end
2. ✅ Deploy backend to Railway
3. ✅ Deploy frontend to Vercel

### Future Enhancements
- [ ] Add user authentication (login/signup)
- [ ] Save session history
- [ ] Allow answering questions
- [ ] Auto-score answers with AI
- [ ] Audio recording for answers
- [ ] Export questions to PDF
- [ ] Dark mode toggle
- [ ] Mobile responsiveness improvements

## Architecture

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   Browser   │ ◄─────► │   Frontend   │ ◄─────► │   Backend   │
│ (React App) │  HTTP   │   (Vite)     │   API   │  (FastAPI)  │
└─────────────┘         └──────────────┘         └─────────────┘
                              │                         │
                              │                         ▼
                              │                  ┌─────────────┐
                              │                  │   Supabase  │
                              │                  │ (PostgreSQL)│
                              │                  └─────────────┘
                              │                         │
                              │                         ▼
                              │                  ┌─────────────┐
                              └─────────────────►│   Gemini    │
                                    (via Backend)│     API     │
                                                  └─────────────┘
```

## Resources

- **Vite Docs**: https://vite.dev/
- **React Docs**: https://react.dev/
- **Tailwind Docs**: https://tailwindcss.com/docs
- **TypeScript Handbook**: https://www.typescriptlang.org/docs/
- **Vercel Docs**: https://vercel.com/docs

---

**Your frontend is ready to use! 🎉**

Start both servers and test the full application flow!
