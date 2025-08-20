from datetime import datetime
from sqlalchemy import Integer, String, Float, DateTime, Index, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .db import Base


class MarketBar(Base):
    __tablename__ = "market_bars"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    symbol: Mapped[str] = mapped_column(String(16), index=True)
    ts: Mapped[datetime] = mapped_column(DateTime, index=True)
    open: Mapped[float] = mapped_column(Float)
    high: Mapped[float] = mapped_column(Float)
    low: Mapped[float] = mapped_column(Float)
    close: Mapped[float] = mapped_column(Float)
    volume: Mapped[float] = mapped_column(Float)

    __table_args__ = (
        UniqueConstraint("symbol", "ts", name="uq_symbol_ts"),
        Index("ix_symbol_ts", "symbol", "ts"),
    )


class BacktestResult(Base):
    __tablename__ = "backtest_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    strategy: Mapped[str] = mapped_column(String(64), index=True)
    symbol: Mapped[str] = mapped_column(String(16), index=True)
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    ended_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    return_pct: Mapped[float] = mapped_column(Float)
    sharpe: Mapped[float] = mapped_column(Float)
    max_drawdown: Mapped[float] = mapped_column(Float)


