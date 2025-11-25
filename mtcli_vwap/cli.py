import click
from .controller import processar_vwap
from .view import exibir_vwap
from .conf import (
    SYMBOL,
    MINUTES,
    LIMIT,
)

@click.command()
@click.version_option(package_name="mtcli-vwap")
@click.option("--symbol", "-s", default=SYMBOL, show_default=True, help="Codigo do ativo.")
@click.option("--minutes", "-m", default=MINUTES, show_default=True, help="Período das barras em minutos.")
@click.option("--limit", "-l", default=LIMIT, show_default=True, help="Número de barras a carregar.")
def vwap(symbol, minutes, limit):
    """
    Calcula o VWAP do ativo SYMBOL com base nas barras intraday.
    """
    resultado = processar_vwap(symbol, minutes, limit)
    exibir_vwap(resultado, symbol)
