from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import requests, analytics
from app.database import engine, Base

# Create all database tables
print("🔧 Creating database tables...")
Base.metadata.create_all(bind=engine)
print("✅ Database tables created successfully!")

# Initialize FastAPI app
app = FastAPI(
    title="GenAI Governance Platform",
    description="AI-Powered Citizen Service Delivery System",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS - Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Allow all headers
)

# Include API routers
app.include_router(
    requests.router, 
    prefix="/api/requests", 
    tags=["Service Requests"]
)

app.include_router(
    analytics.router, 
    prefix="/api/analytics", 
    tags=["Analytics & Dashboard"]
)

# Root endpoint - Health check
@app.get("/", tags=["Health"])
def read_root():
    """
    Root endpoint - Check if API is running
    """
    return {
        "status": "✅ Online",
        "message": "AI-Powered Governance Platform API",
        "version": "1.0.0",
        "endpoints": {
            "docs": "/docs",
            "requests": "/api/requests",
            "analytics": "/api/analytics"
        }
    }


# API Health Check
@app.get("/health", tags=["Health"])
def health_check():
    """
    Health check endpoint for monitoring
    """
    return {
        "status": "healthy",
        "service": "GenAI Governance Platform",
        "database": "connected"
    }


# Startup event
@app.on_event("startup")
async def startup_event():
    """
    Runs when the application starts
    """
    print("=" * 60)
    print("🚀 GenAI Governance Platform API Starting...")
    print("=" * 60)
    print("📍 API Docs: http://127.0.0.1:8000/docs")
    print("📊 Dashboard Analytics: http://127.0.0.1:8000/api/analytics/dashboard")
    print("📝 Submit Request: http://127.0.0.1:8000/api/requests/submit")
    print("=" * 60)


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """
    Runs when the application shuts down
    """
    print("\n👋 GenAI Governance Platform API Shutting down...")
