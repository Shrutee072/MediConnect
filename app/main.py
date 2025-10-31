# from fastapi import FastAPI
# from app.routers import auth, doctor, master, social, posts
# from app.config import settings
# from app.utils.scheduler import start_scheduler, stop_scheduler
# import logging


# logger = logging.getLogger(__name__)

# app = FastAPI(
#     title=settings.PROJECT_NAME,
#     description="FastAPI with PostgreSQL integration for Medical Practice Management",
#     version=settings.VERSION
# )

# # Include routers
# app.include_router(auth.router)
# app.include_router(doctor.router)
# app.include_router(master.router)
# app.include_router(social.router)
# app.include_router(posts.router)

# # Scheduler lifecycle management
# @app.on_event("startup")
# async def startup_event():
#     """Initialize services on app startup"""
#     start_scheduler()

# @app.on_event("shutdown") 
# async def shutdown_event():
#     """Cleanup on app shutdown"""
#     stop_scheduler()

# @app.get("/health")
# async def health():
#     return {"status": "ok", "message": "Medical API is running"}

# @app.get("/")
# async def root():
#     return {
#         "message": "Welcome to Medical API",
#         "version": settings.VERSION,
#         "endpoints": {
#             "authentication": "/auth",
#             "doctor_profile": "/doctor",
#             "master_data": "/master",
#             "social_accounts": "/social",
#             "posts": "/posts",
#             "health_check": "/health",
#             "documentation": "/docs"
#         }
#     }


from fastapi import FastAPI
from app.routers import auth, doctor, master, social, posts
from app.config import settings
from app.utils.scheduler import start_scheduler, stop_scheduler
from app.db import Base, engine
import logging
from app.models import models as doctor_model
from app.models import post as post_model
from app.models import social_account as social_model
from app.routers import UserLogin as userlogin




print("Creating tables if they don't exist...")
Base.metadata.create_all(bind=engine)

logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="FastAPI with PostgreSQL integration for Medical Practice Management",
    version=settings.VERSION
)

app.include_router(userlogin.router)
app.include_router(auth.router)
app.include_router(doctor.router)
app.include_router(master.router)
app.include_router(social.router)
app.include_router(posts.router)

@app.on_event("startup")
async def startup_event():
    """Initialize services on app startup"""
    start_scheduler()

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on app shutdown"""
    stop_scheduler()

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
