"""
Main Entry Point
Runs the FastAPI application
"""

import uvicorn
import os

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("🎯 Support Ticket Classifier API")
    print("=" * 70)
    print("\n📚 Documentation: http://localhost:8000/docs")
    print("❤️  Health Check: http://localhost:8000/health")
    print("📊 API Root: http://localhost:8000")
    print("\n" + "=" * 70 + "\n")
    
    uvicorn.run(
        "src.api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload on code changes
        log_level="info"
    )
