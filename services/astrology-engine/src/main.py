"""
Astrology Engine Service
-----------------------
Main application entry point for the Astrology Engine Service.
This service provides astrological calculations using Swiss Ephemeris.
"""
import time
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from loguru import logger

# Import API routers
from api.birth_chart import router as birth_chart_router
from api.planets import router as planets_router
from api.aspects import router as aspects_router
from api.transits import router as transits_router
from api.progressions import router as progressions_router

# Import configuration
from config import settings

# Create FastAPI application
app = FastAPI(
    title="Astrology Engine Service",
    description="Provides astrological calculations using Swiss Ephemeris",
    version="0.1.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests with timing information."""
    start_time = time.time()
    
    # Get client IP and requested URL
    client_ip = request.client.host
    request_path = request.url.path
    request_method = request.method
    
    # Log the request
    logger.info(f"Request {request_method} {request_path} from {client_ip}")
    
    # Process the request
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        
        # Log response information
        status_code = response.status_code
        logger.info(f"Response {status_code} for {request_method} {request_path} completed in {process_time:.4f}s")
        
        # Add processing time header
        response.headers["X-Process-Time"] = str(process_time)
        return response
    except Exception as e:
        # Log exceptions
        process_time = time.time() - start_time
        logger.error(f"Error processing {request_method} {request_path}: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": {"message": "Internal server error", "code": "INTERNAL_ERROR"}},
        )

# Include API routers
app.include_router(birth_chart_router, prefix="/birth_chart", tags=["Birth Chart"])
app.include_router(planets_router, prefix="/planets", tags=["Planets"])
app.include_router(aspects_router, prefix="/aspects", tags=["Aspects"])
app.include_router(transits_router, prefix="/transits", tags=["Transits"])
app.include_router(progressions_router, prefix="/progressions", tags=["Progressions"])

# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint for monitoring."""
    # TODO: Add more comprehensive health checks (Redis, Ephemeris data, etc.)
    return {"status": "healthy", "service": "astrology-engine"}

# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with service information."""
    return {
        "service": "Astrology Engine",
        "version": "0.1.0",
        "documentation": "/docs",
        "health": "/health",
    }

# Run the application (for development)
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
