from nicegui import app, ui
import httpx
import os

BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")


async def fetch_health() -> str:
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{BACKEND_URL}/health")
        r.raise_for_status()
        return r.json().get("status", "unknown")


async def ingest(symbol: str) -> None:
    async with httpx.AsyncClient() as client:
        await client.post(f"{BACKEND_URL}/data/ingest", params={"symbol": symbol, "period": "1mo", "interval": "1h"})


async def fetch_signals(symbol: str):
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{BACKEND_URL}/signals/sma", params={"symbol": symbol})
        r.raise_for_status()
        return r.json().get("signals", [])


symbol_state = ui.state("AAPL")

with ui.header():
    ui.label("ZQuantTrader Dashboard")

with ui.row().style("margin: 1rem;"):
    symbol_input = ui.input("Symbol", value=symbol_state.value).on_value_change(lambda e: symbol_state.set(e.value))
    ui.button("Ingest 1mo 1h", on_click=lambda: ingest(symbol_state.value))
    status_label = ui.label("Health: ...")


async def update_health():
    status = await fetch_health()
    status_label.text = f"Health: {status}"


@ui.page("/")
def index():
    with ui.column():
        ui.label("Simple SMA Signals")
        signals_table = ui.table({
            "ts": "Timestamp",
            "signal": "Signal"
        }, rows=[])

        async def refresh():
            rows = await fetch_signals(symbol_state.value)
            signals_table.rows = rows[-50:]

        ui.button("Refresh Signals", on_click=refresh)
        ui.timer(5.0, update_health)


ui.run(host="0.0.0.0", port=3000, reload=False)


