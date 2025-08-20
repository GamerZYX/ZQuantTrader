from typing import List

import pandas as pd
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import MarketBar
from ..strategies.sma import simple_moving_average_signal

router = APIRouter()


@router.get("/sma")
def sma_signals(symbol: str, window_short: int = 5, window_long: int = 20, limit: int = 300, db: Session = Depends(get_db)) -> dict:
    q = (
        db.query(MarketBar)
        .filter(MarketBar.symbol == symbol.upper())
        .order_by(MarketBar.ts.asc())
        .limit(limit)
    )
    rows = q.all()
    if not rows:
        return {"signals": []}
    df = pd.DataFrame([
        {"ts": r.ts, "close": r.close} for r in rows
    ]).set_index("ts").sort_index()
    signals = simple_moving_average_signal(df["close"], window_short=window_short, window_long=window_long)
    out: List[dict] = [
        {"ts": ts.isoformat(), "signal": int(sig)} for ts, sig in signals.items()
    ]
    return {"signals": out}


