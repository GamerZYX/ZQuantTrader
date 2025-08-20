from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .db import init_engine_and_tables
from .routers.health import router as health_router
from .routers.data import router as data_router
from .routers.signals import router as signals_router
from .routers.backtest import router as backtest_router


app = FastAPI(title="ZQuantTrader API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    init_engine_and_tables()


app.include_router(health_router, prefix="/health", tags=["health"]) 
app.include_router(data_router, prefix="/data", tags=["data"]) 
app.include_router(signals_router, prefix="/signals", tags=["signals"]) 
app.include_router(backtest_router, prefix="/backtest", tags=["backtest"]) 


