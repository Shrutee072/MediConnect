from fastapi import FastAPI
from app.routers import auth, doctor, master, social, posts
from app.config import settings
from app.utils.scheduler import start_scheduler, stop_scheduler
import atexit

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="FastAPI with PostgreSQL integration for Medical Practice Management",
    version=settings.VERSION
)

# Include routers
app.include_router(auth.router)
app.include_router(doctor.router)
app.include_router(master.router)
app.include_router(social.router)
app.include_router(posts.router)

# Start the post scheduler
start_scheduler()

# Register cleanup function
atexit.register(stop_scheduler)

@app.get("/health")
async def health():
    return {"status": "ok", "message": "Medical API is running"}

@app.get("/")
async def root():
    return {
        "message": "Welcome to Medical API",
        "version": settings.VERSION,
        "endpoints": {
            "authentication": "/auth",
            "doctor_profile": "/doctor",
            "master_data": "/master",
            "social_accounts": "/social",
            "posts": "/posts",
            "health_check": "/health",
            "documentation": "/docs"
        }
    }