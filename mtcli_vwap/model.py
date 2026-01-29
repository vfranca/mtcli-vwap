# ============================
# mtcli_vwap/model.py
# ============================
import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime, timedelta
from mtcli.mt5_context import mt5_conexao
from mtcli.logger import setup_logger

log = setup_logger()


def calcular_vwap(
    symbol: str,
    minutes: int,
    limit: int,
    anchor_type: str = "abertura",
    anchor_time: datetime | None = None,
    bandas: int = 0,
):
    """
    Calcula a VWAP (Volume Weighted Average Price) a partir dos dados do MT5.

    Suporta VWAP ancorada e bandas de desvio padrão.

    :return: dict com resultado estruturado ou None
    """
    with mt5_conexao():
        if not mt5.symbol_select(symbol, True):
            log.error(f"Erro ao selecionar símbolo {symbol}")
            return None

        timeframe = _get_timeframe(minutes)
        utc_from = datetime.now() - timedelta(minutes=limit * minutes)
        rates = mt5.copy_rates_from(symbol, timeframe, utc_from, limit)

        if rates is None or len(rates) == 0:
            log.warning(f"Sem dados para VWAP {symbol}")
            return None

    df = pd.DataFrame(rates)
    df["datetime"] = pd.to_datetime(df["time"], unit="s")

    # Ancoragem
    if anchor_type == "hora" and anchor_time:
        df = df[df["datetime"] >= anchor_time]

    # Preço típico e VWAP
    df["tp"] = (df["high"] + df["low"] + df["close"]) / 3
    df["pv"] = df["tp"] * df["real_volume"]
    df["vwap"] = df["pv"].cumsum() / df["real_volume"].cumsum()

    resultado = {
        "vwap": float(df["vwap"].iloc[-1]),
        "anchor_type": anchor_type,
        "anchor_time": anchor_time.isoformat() if anchor_time else None,
    }

    # Bandas de desvio padrão
    if bandas > 0:
        df["desvio"] = (df["tp"] - df["vwap"]) ** 2
        df["std"] = (df["desvio"].cumsum() / (df.index + 1)).pow(0.5)

        for i in range(1, bandas + 1):
            resultado[f"banda_sup_{i}"] = float(df["vwap"].iloc[-1] + i * df["std"].iloc[-1])
            resultado[f"banda_inf_{i}"] = float(df["vwap"].iloc[-1] - i * df["std"].iloc[-1])

    return resultado


def _get_timeframe(minutes: int):
    """Converte minutos para timeframe do MetaTrader 5."""
    return {
        1: mt5.TIMEFRAME_M1,
        2: mt5.TIMEFRAME_M2,
        3: mt5.TIMEFRAME_M3,
        5: mt5.TIMEFRAME_M5,
        10: mt5.TIMEFRAME_M10,
        15: mt5.TIMEFRAME_M15,
        30: mt5.TIMEFRAME_M30,
        60: mt5.TIMEFRAME_H1,
        120: mt5.TIMEFRAME_H2,
        240: mt5.TIMEFRAME_H4,
    }.get(minutes, mt5.TIMEFRAME_M1)
