from datetime import datetime
from typing import List, Optional

import pandas as pd
import yfinance as yf
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import MarketBar

router = APIRouter()


@router.post("/ingest")
def ingest(symbol: str, period: str = "1mo", interval: str = "1h", db: Session = Depends(get_db)) -> dict:
    df = yf.download(symbol, period=period, interval=interval, progress=False)
    if df.empty:
        return {"ingested": 0}
    df = df.reset_index()
    records = []
    for _, row in df.iterrows():
        ts: datetime = pd.to_datetime(row["Datetime"] if "Datetime" in row else row["Date"]).to_pydatetime()
        bar = MarketBar(
            symbol=symbol.upper(),
            ts=ts,
            open=float(row["Open"]),
            high=float(row["High"]),
            low=float(row["Low"]),
            close=float(row["Close"]),
            volume=float(row.get("Volume", 0.0)),
        )
        records.append(bar)
    # Upsert-like behavior: try insert; ignore duplicates
    inserted = 0
    for bar in records:
        try:
            db.add(bar)
            db.commit()
            inserted += 1
        except Exception:
            db.rollback()
    return {"ingested": inserted}


@router.get("/bars", response_model=List[dict])
def get_bars(symbol: str, limit: int = Query(100, le=1000), db: Session = Depends(get_db)) -> List[dict]:
    q = (
        db.query(MarketBar)
        .filter(MarketBar.symbol == symbol.upper())
        .order_by(MarketBar.ts.desc())
        .limit(limit)
    )
    rows = q.all()
    return [
        {
            "symbol": r.symbol,
            "ts": r.ts.isoformat(),
            "open": r.open,
            "high": r.high,
            "low": r.low,
            "close": r.close,
            "volume": r.volume,
        }
        for r in rows
    ]


