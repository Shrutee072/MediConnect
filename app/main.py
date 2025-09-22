from fastapi import FastAPI

app = FastAPI(title="Medical API", description="FastAPI with PostgreSQL integration")

@app.get("/health")
async def health():
    return {"status": "ok", "message": "Medical API is running"}

@app.get("/")
async def root():
    return {"message": "Welcome to Medical API"}