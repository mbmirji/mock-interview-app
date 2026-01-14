# Updated Upload Flow - Job Description as File + Additional Context ✅

## What Changed

The upload flow has been updated to accept:
1. **Resume file** (PDF, DOC, DOCX)
2. **Job description file** (PDF, DOC, DOCX, TXT)
3. **Additional context** (optional text field)

## Changes Made

### Frontend Updates

#### 1. UploadPage Component ([frontend/src/pages/UploadPage.tsx](frontend/src/pages/UploadPage.tsx))

**New State:**
```typescript
const [resumeFile, setResumeFile] = useState<File | null>(null);
const [jobDescFile, setJobDescFile] = useState<File | null>(null);
const [additionalContext, setAdditionalContext] = useState('');
```

**New UI Elements:**
- Resume file upload section
- Job description file upload section
- Additional context textarea (optional)
- Visual feedback showing selected files

**File Type Support:**
- Resume: `.pdf, .doc, .docx`
- Job Description: `.pdf, .doc, .docx, .txt`

#### 2. API Service ([frontend/src/services/api.ts](frontend/src/services/api.ts))

**Updated Function Signature:**
```typescript
export const uploadResumeAndJobDescription = async (
  resumeFile: File,
  jobDescFile: File,
  additionalContext: string
): Promise<UploadResponse>
```

**FormData Structure:**
```typescript
formData.append('resume_file', resumeFile);
formData.append('job_desc_file', jobDescFile);
formData.append('additional_context', additionalContext);
```

### Backend Updates

#### 1. New Text Extraction Function ([backend/app/api/endpoints/__init__.py](backend/app/api/endpoints/__init__.py))

```python
def extract_text_from_file(file_bytes: bytes, filename: str) -> str:
    """Extract text from PDF, DOC, DOCX, or TXT file"""
    file_ext = filename.lower().rsplit(".", 1)[-1]

    if file_ext == "pdf":
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            return "\n".join([page.extract_text() or "" for page in pdf.pages])
    elif file_ext in ["doc", "docx"]:
        doc = Document(io.BytesIO(file_bytes))
        return "\n".join([para.text for para in doc.paragraphs])
    elif file_ext == "txt":
        return file_bytes.decode("utf-8")
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported file format: .{file_ext}")
```

#### 2. Updated Upload Endpoint

**New Parameters:**
```python
@router.post("/upload")
async def upload_documents(
    resume_file: UploadFile = File(...),
    job_desc_file: UploadFile = File(...),
    additional_context: str = Form(""),
    llm_service: LLMService = Depends(get_llm_service),
):
```

**Context Handling:**
```python
# Combine job description with additional context if provided
full_context = job_desc_content
if additional_context and additional_context.strip():
    full_context += f"\n\nADDITIONAL CONTEXT:\n{additional_context.strip()}"

# Pass to LLM
questions_answers = llm_service.generate_interview_questions(
    resume_content, full_context
)
```

**Response Format:**
```python
return {
    "success": True,
    "message": "Interview questions generated successfully",
    "resume_filename": resume_file.filename,
    "job_desc_filename": job_desc_file.filename,
    "questions_count": len(questions_answers),
    "questions": questions_answers
}
```

## New User Flow

### Step 1: Upload Resume
- Click or drag-and-drop resume file
- Accepts: PDF, DOC, DOCX
- Max size: 10MB
- Visual confirmation when file selected

### Step 2: Upload Job Description
- Click or drag-and-drop job description file
- Accepts: PDF, DOC, DOCX, TXT
- Max size: 10MB
- Visual confirmation when file selected

### Step 3: Add Context (Optional)
User can add additional information like:
- Years of experience with specific technologies
- Areas to focus on (e.g., "Focus on system design")
- Specific interests (e.g., "Interested in cloud architecture roles")
- Gaps or strengths to highlight

**Example:**
```
I have 2 years of experience with microservices architecture.
Focus on distributed systems and scalability questions.
I'm particularly interested in senior backend engineering roles.
```

### Step 4: Generate Questions
- Both files required before submit button activates
- Loading state shown during generation (10-30 seconds)
- Questions displayed on success

## Benefits

### For Users

✅ **Easier Job Description Entry**
- No copy-pasting required
- Can upload company's job posting PDF directly
- Handles formatted documents

✅ **Better Context**
- Additional context helps LLM generate more relevant questions
- Can highlight specific areas of interest
- Can provide background not in resume

✅ **More Flexibility**
- Support for multiple file formats
- Optional context field (not required)
- Clear visual feedback

### For System

✅ **Better Text Extraction**
- Reusable `extract_text_from_file()` function
- Support for TXT files (simpler format)
- Consistent error handling

✅ **Enhanced LLM Prompts**
- More context = better questions
- Clearly separated additional context
- LLM can tailor questions to user's focus areas

## Example Requests

### With Additional Context

```bash
curl -X POST http://localhost:8001/api/v1/upload \
  -F "resume_file=@resume.pdf" \
  -F "job_desc_file=@job_description.pdf" \
  -F "additional_context=I have 2 years microservices experience. Focus on system design."
```

### Without Additional Context

```bash
curl -X POST http://localhost:8001/api/v1/upload \
  -F "resume_file=@resume.pdf" \
  -F "job_desc_file=@job_description.txt" \
  -F "additional_context="
```

## Response Example

```json
{
  "success": true,
  "message": "Interview questions generated successfully",
  "resume_filename": "john_doe_resume.pdf",
  "job_desc_filename": "senior_engineer_jd.pdf",
  "questions_count": 15,
  "questions": [
    {
      "question": "Given your background in microservices, describe how you would design a highly available distributed system...",
      "answer": "A strong candidate would discuss service discovery, load balancing, circuit breakers..."
    }
  ]
}
```

## Testing

### Test Case 1: Both Files + Context

**Input:**
- Resume: PDF file
- Job Desc: PDF file
- Context: "Focus on system design and scalability"

**Expected:** Questions tailored to system design

### Test Case 2: Both Files, No Context

**Input:**
- Resume: DOCX file
- Job Desc: TXT file
- Context: (empty)

**Expected:** Questions based only on resume + JD

### Test Case 3: Missing Job Description

**Input:**
- Resume: PDF file
- Job Desc: (none)

**Expected:** Error message "Please select a job description file"

### Test Case 4: Invalid File Type

**Input:**
- Resume: PDF file
- Job Desc: JPG image

**Expected:** Error "Invalid job description file type"

## UI Features

### Visual Feedback

✅ File names shown after selection
✅ Green checkmark when file selected
✅ Disabled submit button until both files selected
✅ Loading spinner during generation
✅ Success message with question count
✅ Error messages with clear descriptions

### Usability

✅ Drag-and-drop support
✅ Clear labels with asterisks for required fields
✅ Helper text explaining what to enter
✅ Example context provided
✅ Reset button to start over

## Migration Notes

### Breaking Changes

⚠️ **API Parameters Changed:**
- Old: `file`, `job_description` (text)
- New: `resume_file`, `job_desc_file`, `additional_context`

⚠️ **Frontend Must Update:**
- Must send two files instead of one file + text
- Must use new parameter names

### Backward Compatibility

❌ **Not backward compatible** - old clients will get 422 errors

**Why:** Complete parameter change requires coordinated frontend + backend deployment

## Deployment Steps

### Step 1: Deploy Backend
```bash
cd backend
git pull
./start.sh
```

Backend will run on http://localhost:8001

### Step 2: Deploy Frontend
```bash
cd frontend
git pull
npm install  # If new dependencies
npm run dev
```

Frontend will run on http://localhost:5173

### Step 3: Test End-to-End

1. Upload resume PDF
2. Upload job description PDF
3. Add context: "2 years Python experience"
4. Generate questions
5. Verify questions appear

## Troubleshooting

### Error: "Invalid job description file type"

**Cause:** Uploaded file not in allowed formats

**Solution:** Use PDF, DOC, DOCX, or TXT files

### Error: "Could not extract text from file"

**Possible causes:**
- PDF is image-based (scanned document)
- File is password protected
- File is corrupted

**Solution:**
- Use text-based PDFs
- Remove password protection
- Try different file format

### Context Not Affecting Questions

**Check:**
1. Context field has text
2. Backend logs show context being passed
3. Try more specific context

**Example Good Context:**
```
I have 5 years of Python and FastAPI experience.
I want to focus on scalability and distributed systems.
Please include questions about microservices architecture.
```

## File Size Limits

- Resume: Max 10MB
- Job Description: Max 10MB
- Additional Context: No limit (text only)

## Supported File Formats

| File Type | Resume | Job Description |
|-----------|--------|-----------------|
| PDF       | ✅     | ✅              |
| DOC       | ✅     | ✅              |
| DOCX      | ✅     | ✅              |
| TXT       | ❌     | ✅              |

---

**All changes are complete and ready to test!** 🚀
