# -*- coding: utf-8 -*-
"""Exemplo de robô de trading com múltiplos indicadores.

Este script se conecta à Binance usando as chaves de API definidas em
variáveis de ambiente e executa ordens de compra e venda de forma
automatizada com base em sinais de indicadores técnicos.

Indicadores utilizados:
- Médias móveis exponenciais (curta e longa)
- MACD (Moving Average Convergence Divergence)
- RSI (Relative Strength Index)
- Bandas de Bollinger

Este exemplo é fornecido para fins educacionais e não constitui
aconselhamento financeiro. Negociar ativos digitais envolve riscos.
"""

import os
import time
from typing import Optional

import pandas as pd
from binance.client import Client
from binance.exceptions import BinanceAPIException
import ta

# Chaves de API
#
# Para facilitar o exemplo, as credenciais abaixo já estão definidas.
# Você pode sobrescrevê-las por variáveis de ambiente BINANCE_KEY e
# BINANCE_SECRET, caso prefira mantê-las fora do código.
BINANCE_KEY = os.getenv(
    "BINANCE_KEY",
    "jd65rfykiMAn7XCmuHExhFvicrSciIj2N28HthYG5kvectR2LRcgSE0GepidVAxv",
)
BINANCE_SECRET = os.getenv(
    "BINANCE_SECRET",
    "n5pBy1zGWxn2HYtpvNk84gX34OLrwnQ2I7H4iKOo3JMbC8GVQVelF37OHRjvSAlu",
)

# Inicializa o cliente da Binance
client = Client(BINANCE_KEY, BINANCE_SECRET)

# Configurações da estratégia
SYMBOL = "PEPEUSDT"
INTERVAL = Client.KLINE_INTERVAL_1MINUTE
WINDOW_EMA_SHORT = 12
WINDOW_EMA_LONG = 26
RSI_PERIOD = 14
RSI_OVERSOLD = 30
RSI_OVERBOUGHT = 70
BOLLINGER_WINDOW = 20
BOLLINGER_STD = 2
MAX_RISK_USDT = 1.0  # Valor máximo arriscado por operação


def obter_dados(limite: int = 200) -> pd.DataFrame:
    """Busca dados de candles e retorna DataFrame com colunas relevantes."""
    klines = client.get_historical_klines(SYMBOL, INTERVAL, f"{limite} minutes ago UTC")
    df = pd.DataFrame(klines, columns=[
        "open_time", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "number_of_trades",
        "taker_buy_base_volume", "taker_buy_quote_volume", "ignore"
    ])
    df["close"] = pd.to_numeric(df["close"])
    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
    df.set_index("open_time", inplace=True)
    return df[["close"]]


def analisar_mercado(df: pd.DataFrame) -> str:
    """Gera sinal de compra ou venda com base nos indicadores."""
    df["ema_short"] = ta.trend.ema_indicator(df["close"], window=WINDOW_EMA_SHORT)
    df["ema_long"] = ta.trend.ema_indicator(df["close"], window=WINDOW_EMA_LONG)
    macd = ta.trend.MACD(df["close"], window_slow=26, window_fast=12, window_sign=9)
    df["macd"] = macd.macd()
    df["macd_signal"] = macd.macd_signal()
    df["rsi"] = ta.momentum.rsi(df["close"], window=RSI_PERIOD)
    bollinger = ta.volatility.BollingerBands(df["close"], window=BOLLINGER_WINDOW, window_dev=BOLLINGER_STD)
    df["bb_high"] = bollinger.bollinger_hband()
    df["bb_low"] = bollinger.bollinger_lband()

    df.dropna(inplace=True)
    ultimo = df.iloc[-1]
    anterior = df.iloc[-2]

    # Sinais de cruzamento de EMAs
    cruzamento_compra = ultimo["ema_short"] > ultimo["ema_long"] and anterior["ema_short"] <= anterior["ema_long"]
    cruzamento_venda = ultimo["ema_short"] < ultimo["ema_long"] and anterior["ema_short"] >= anterior["ema_long"]

    # Sinais de MACD
    macd_compra = ultimo["macd"] > ultimo["macd_signal"] and anterior["macd"] <= anterior["macd_signal"]
    macd_venda = ultimo["macd"] < ultimo["macd_signal"] and anterior["macd"] >= anterior["macd_signal"]

    # Condições de RSI e bandas de Bollinger
    sobrevendido = ultimo["rsi"] < RSI_OVERSOLD and ultimo["close"] < ultimo["bb_low"]
    sobrecomprado = ultimo["rsi"] > RSI_OVERBOUGHT and ultimo["close"] > ultimo["bb_high"]

    # Combina sinal de EMAs e MACD
    if (cruzamento_compra or macd_compra) and not sobrecomprado:
        return "comprar"
    elif (cruzamento_venda or macd_venda) and not sobrevendido:
        return "vender"
    else:
        return "manter"


def tamanho_posicao(preco: float, valor_usdt: float) -> float:
    """Define tamanho de posicao em PEPE de acordo com o risco."""
    return valor_usdt / preco


def executar_ordem(acao: str, quantidade_usdt: float) -> Optional[dict]:
    """Envia ordem de mercado de compra ou venda."""
    try:
        if acao == "comprar":
            order = client.order_market_buy(symbol=SYMBOL, quoteOrderQty=quantidade_usdt)
        elif acao == "vender":
            # Para vender, convertemos quantidade de USDT para moeda PEPE
            saldo_pepe = float(client.get_asset_balance(asset="PEPE")["free"])
            if saldo_pepe <= 0:
                print("Sem saldo PEPE para vender.")
                return None
            order = client.order_market_sell(symbol=SYMBOL, quantity=saldo_pepe)
        else:
            return None
        print("Ordem executada:", order)
        return order
    except BinanceAPIException as e:
        print("Erro ao enviar ordem:", e)
        return None


def robo_trader():
    """Loop principal do rob\u00f4."""
    print("Iniciando rob\u00f4 profissional...")
    while True:
        df = obter_dados()
        acao = analisar_mercado(df)
        preco_atual = df["close"].iloc[-1]

        if acao in ["comprar", "vender"]:
            quantidade_usdt = MAX_RISK_USDT
            executar_ordem(acao, quantidade_usdt)
        else:
            print("Sem sinal no momento. Pre\u00e7o atual:", preco_atual)

        # Aguarda o pr\u00f3ximo candle
        time.sleep(60)


if __name__ == "__main__":
    robo_trader()
