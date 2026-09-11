import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import analytics, machines, tickets

app = FastAPI(title="Predictive Maintenance API")

# ALLOWED_ORIGINS 支持逗号分隔的多个来源，本地开发默认放行 5173
_allowed_origins = os.environ.get("ALLOWED_ORIGINS", "http://localhost:5173")
allow_origins = [origin.strip() for origin in _allowed_origins.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(machines.router)
app.include_router(analytics.router)
app.include_router(tickets.router)


@app.get("/api/health")
def health():
    return {"status": "ok"}
