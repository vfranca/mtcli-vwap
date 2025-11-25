import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime, timedelta

def conecta():
    if not mt5.initialize():
        raise RuntimeError("Falha ao conectar ao MetaTrader 5.")

def calcular_vwap(symbol, minutes, limit):
    conecta()

    timeframe = _get_timeframe(minutes)
    utc_from = datetime.now() - timedelta(minutes=limit * minutes)

    rates = mt5.copy_rates_from(symbol, timeframe, utc_from, limit)
    if rates is None or len(rates) == 0:
        return None

    df = pd.DataFrame(rates)
    df["tp"] = (df["high"] + df["low"] + df["close"]) / 3
    df["vwap_num"] = df["tp"] * df["real_volume"]
    df["vwap_den"] = df["real_volume"]
    df["vwap"] = df["vwap_num"].cumsum() / df["vwap_den"].cumsum()

    return df["vwap"].iloc[-1]

def _get_timeframe(minutes):
    return {
        1: mt5.TIMEFRAME_M1,
        5: mt5.TIMEFRAME_M5,
        15: mt5.TIMEFRAME_M15,
        30: mt5.TIMEFRAME_M30,
        60: mt5.TIMEFRAME_H1
    }.get(minutes, mt5.TIMEFRAME_M1)
