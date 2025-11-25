from .model import calcular_vwap


def processar_vwap(symbol, minutes, limit):
    return calcular_vwap(symbol, minutes, limit)
