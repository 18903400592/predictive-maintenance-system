import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.db import engine
from app.routers import analytics, machines, tickets
from scripts.load_data import load_data


def _init_data_if_empty():
    """服务启动时若 machines 表为空，则从 CSV 自动加载初始数据（幂等，仅在空表时执行）。"""
    with engine.connect() as conn:
        count = conn.execute(text("SELECT count(*) FROM machines")).scalar()

    if count == 0:
        print("machines 表为空，正在从 CSV 加载初始数据...")
        load_data(engine)
    else:
        print(f"machines 表已有 {count} 条记录，跳过初始化")


@asynccontextmanager
async def lifespan(app: FastAPI):
    _init_data_if_empty()
    yield


app = FastAPI(title="Predictive Maintenance API", lifespan=lifespan)

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
