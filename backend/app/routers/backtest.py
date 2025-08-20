from typing import List

import numpy as np
import pandas as pd
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import MarketBar, BacktestResult
from ..strategies.sma import simple_moving_average_signal

router = APIRouter()


@router.post("/sma")
def backtest_sma(symbol: str, window_short: int = 5, window_long: int = 20, db: Session = Depends(get_db)) -> dict:
    rows = (
        db.query(MarketBar)
        .filter(MarketBar.symbol == symbol.upper())
        .order_by(MarketBar.ts.asc())
        .all()
    )
    if not rows:
        return {"message": "no data"}
    df = pd.DataFrame([{ "ts": r.ts, "close": r.close } for r in rows]).set_index("ts").sort_index()

    signals = simple_moving_average_signal(df["close"], window_short, window_long)
    df = df.join(signals.rename("signal"), how="left").fillna(0)
    df["ret"] = df["close"].pct_change().fillna(0)
    df["strat_ret"] = df["ret"] * df["signal"].shift(1).fillna(0)
    cum_return = (1 + df["strat_ret"]).prod() - 1
    sharpe = (df["strat_ret"].mean() / (df["strat_ret"].std() + 1e-9)) * np.sqrt(252)
    cum_curve = (1 + df["strat_ret"]).cumprod()
    running_max = cum_curve.cummax()
    drawdown = (cum_curve / (running_max + 1e-9)) - 1
    mdd = drawdown.min()

    result = BacktestResult(
        strategy="sma",
        symbol=symbol.upper(),
        return_pct=float(cum_return),
        sharpe=float(sharpe),
        max_drawdown=float(mdd),
    )
    db.add(result)
    db.commit()

    return {
        "metrics": {
            "return_pct": float(cum_return),
            "sharpe": float(sharpe),
            "max_drawdown": float(mdd),
        },
        "equity_curve": [
            {"ts": ts.isoformat(), "equity": float(val)} for ts, val in cum_curve.items()
        ],
    }


