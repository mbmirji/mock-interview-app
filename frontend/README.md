# Mock Interview App - Frontend

React + TypeScript + Vite + Tailwind CSS frontend for the Mock Interview application.

## Features

- Upload resume (PDF, DOC, DOCX)
- Enter job description
- Generate personalized interview questions using AI
- View questions with reference answers
- Clean, modern UI with Tailwind CSS
- TypeScript for type safety

## Tech Stack

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Styling
- **Axios** - HTTP client
- **React Router** - Routing (ready for future expansion)

## Getting Started

### Prerequisites

- Node.js 18+ installed
- Backend server running on `http://localhost:8000`

### Installation

```bash
# Install dependencies
npm install
```

### Configuration

Create a `.env` file (or use the existing one):

```env
VITE_API_URL=http://localhost:8000
```

### Development

```bash
# Start development server
npm run dev
```

The app will be available at `http://localhost:5173`

### Build for Production

```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

## Project Structure

```
frontend/
├── src/
│   ├── components/       # Reusable components
│   │   ├── FileUpload.tsx
│   │   └── QuestionList.tsx
│   ├── pages/            # Page components
│   │   └── UploadPage.tsx
│   ├── services/         # API services
│   │   └── api.ts
│   ├── types/            # TypeScript types
│   │   └── index.ts
│   ├── App.tsx           # Main app component
│   ├── main.tsx          # Entry point
│   └── index.css         # Global styles
├── public/               # Static assets
├── .env                  # Environment variables
├── package.json
├── tsconfig.json
├── vite.config.ts
└── tailwind.config.js
```

## Components

### FileUpload

Drag-and-drop file upload component with validation:
- Accepts PDF, DOC, DOCX files
- Max size: 10MB
- Drag and drop support
- File type and size validation

### QuestionList

Displays generated interview questions:
- Question numbering
- Question text
- Reference answers
- Support for user answers and scores (future feature)

### UploadPage

Main page that combines:
- File upload
- Job description input
- Question generation
- Question display

## API Integration

The frontend communicates with the backend using Axios:

```typescript
// Upload resume and job description
uploadResumeAndJobDescription(file, jobDescription)

// Get interview session
getInterviewSession(sessionId)
```

## Deployment to Vercel

### Quick Deploy

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Add frontend"
   git push
   ```

2. **Deploy to Vercel**:
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project"
   - Import your GitHub repository
   - Set root directory to `frontend`
   - Add environment variable:
     - `VITE_API_URL` = your backend URL (e.g., Railway deployment URL)
   - Click "Deploy"

### Environment Variables for Production

In Vercel dashboard, add:

```env
VITE_API_URL=https://your-backend-url.railway.app
```

### Build Configuration

Vercel will auto-detect Vite and use these settings:
- Build Command: `npm run build`
- Output Directory: `dist`
- Install Command: `npm install`

## CORS Configuration

Make sure your backend allows requests from your frontend domain. In your backend's `main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",           # Local development
        "https://your-app.vercel.app"      # Production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## File Validation

The frontend validates files before upload:
- **Allowed formats**: PDF (.pdf), Word (.doc, .docx)
- **Max size**: 10MB
- **Error messages**: User-friendly validation errors

Server-side validation is still performed by the backend.

## Future Enhancements

- [ ] User authentication
- [ ] Session history
- [ ] Answer submission and scoring
- [ ] Audio recording for answers
- [ ] Dark mode
- [ ] Multi-language support
- [ ] Progress tracking
- [ ] Export questions to PDF

## Troubleshooting

### Backend Connection Issues

If you see "Failed to upload" errors:

1. Check backend is running: `http://localhost:8000/health`
2. Verify `VITE_API_URL` in `.env`
3. Check browser console for CORS errors
4. Ensure backend CORS allows your frontend origin

### Build Errors

```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Clear Vite cache
rm -rf node_modules/.vite
```

### TypeScript Errors

```bash
# Check types
npm run type-check

# Fix TypeScript errors
npx tsc --noEmit
```

## Scripts

```bash
# Development
npm run dev          # Start dev server

# Build
npm run build        # Build for production
npm run preview      # Preview production build

# Linting
npm run lint         # Lint code
```

## License

MIT

## Support

For issues or questions, please open an issue on GitHub.
