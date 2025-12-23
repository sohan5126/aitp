from pydantic import BaseModel
from typing import List, Optional

class Tag(BaseModel):
    label: str
    confidence: float

class AnalysisResponse(BaseModel):
    filename: str
    tags: List[Tag]
    description: Optional[str] = None
    processing_time: float

class HealthCheck(BaseModel):
    status: str
