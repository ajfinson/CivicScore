"""FastAPI app startup"""
from fastapi import FastAPI
from app.api import routes_reports, routes_issues, routes_scores, routes_health

app = FastAPI(title="CivicPulse Engine", version="0.1.0")

# Include routers
app.include_router(routes_health.router)
app.include_router(routes_reports.router)
app.include_router(routes_issues.router)
app.include_router(routes_scores.router)

@app.get("/")
async def root():
    return {"message": "CivicPulse Engine API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
