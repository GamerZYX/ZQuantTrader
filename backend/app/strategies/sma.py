import pandas as pd


def simple_moving_average_signal(close: pd.Series, window_short: int = 5, window_long: int = 20) -> pd.Series:
    close = close.sort_index()
    ma_s = close.rolling(window_short, min_periods=1).mean()
    ma_l = close.rolling(window_long, min_periods=1).mean()
    signal = (ma_s > ma_l).astype(int) - (ma_s < ma_l).astype(int)
    return signal


