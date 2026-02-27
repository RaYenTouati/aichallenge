from pydantic import BaseModel
from typing import List, Optional

class SourceInfo(BaseModel):
    document_name: str
    content_snippet: str
    confidence_score: float

class QueryRequest(BaseModel):
    question: str
    generate_email: bool = False

class QueryResponse(BaseModel):
    answer: str
    sources: List[SourceInfo]
    fallback_used: bool
