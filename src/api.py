"""
FastAPI Application
RESTful API for ticket classification
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict
from src.classifier import TicketClassifier

# Initialize FastAPI
app = FastAPI(
    title="Support Ticket Classifier",
    description="AI-powered ticket classification using Endee vector search",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize classifier (loaded once on startup)
classifier = None


@app.on_event("startup")
async def startup_event():
    """Load classifier on startup"""
    global classifier
    print("\n🚀 Starting Support Ticket Classifier API...")
    classifier = TicketClassifier()
    print("✅ API ready!\n")


# Request/Response Models
class TicketRequest(BaseModel):
    """Ticket classification request"""
    text: str = Field(
        ...,
        min_length=10,
        max_length=2000,
        description="Ticket description"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "text": "I forgot my password and the reset link isn't working"
            }
        }


class SimilarTicket(BaseModel):
    """Similar ticket information"""
    text: str
    category: str
    priority: str
    similarity: float


class ClassificationResponse(BaseModel):
    """Classification result"""
    category: str
    priority: str
    confidence: float
    routing_team: str
    similar_tickets: List[SimilarTicket]


# API Endpoints
@app.get("/")
async def root():
    """API information"""
    return {
        "message": "Support Ticket Classifier API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "classifier": "ready" if classifier else "not ready"
    }


@app.post("/classify", response_model=ClassificationResponse)
async def classify_ticket(request: TicketRequest):
    """
    Classify a support ticket
    
    Returns category, priority, confidence, and routing information
    """
    if not classifier:
        raise HTTPException(
            status_code=503,
            detail="Classifier not initialized"
        )
    
    try:
        result = classifier.classify(request.text)
        return ClassificationResponse(**result)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Classification error: {str(e)}"
        )


@app.get("/categories")
async def get_categories():
    """Get list of available ticket categories"""
    if not classifier:
        raise HTTPException(
            status_code=503,
            detail="Classifier not initialized"
        )
    
    return {
        "categories": classifier.get_categories()
    }


@app.get("/stats")
async def get_stats():
    """Get index statistics from Endee"""
    if not classifier:
        raise HTTPException(
            status_code=503,
            detail="Classifier not initialized"
        )
    
    stats = classifier.endee.get_stats("support_tickets")
    return stats
