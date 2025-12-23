import time
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .models import AnalysisResponse, HealthCheck
from .ai_service import AIService
import os

app = FastAPI(title="AI Photo Tagger API")

# Enable CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For local dev allow all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize AI Service
ai_service = AIService()

# Mount frontend files to serve them directly (Optional, good for simple deployment)
# We will create the directory if it doesn't exist to avoid errors on fresh start
if not os.path.exists("frontend"):
    os.makedirs("frontend")

app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/health", response_model=HealthCheck)
async def health_check():
    return HealthCheck(status="ok")

@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_image(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    start_time = time.time()
    
    try:
        content = await file.read()
        tags = await ai_service.analyze_image(content)
        
        processing_time = time.time() - start_time
        
        return AnalysisResponse(
            filename=file.filename,
            tags=tags,
            description="AI analysis completed successfully.",
            processing_time=processing_time
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def read_index():
    from fastapi.responses import FileResponse
    return FileResponse('frontend/index.html')
