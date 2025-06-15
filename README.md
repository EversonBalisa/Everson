# Robô de Trading - Exemplo Profissional

Este repositório inclui um exemplo de robô de trading para a Binance
usando Python. O script `pro_trading_bot.py` demonstra como combinar
indicadores técnicos (EMAs, MACD, RSI e Bandas de Bollinger) para gerar
sinais de compra e venda da moeda PEPE/USDT.

## Requisitos
- Python 3.8+
- Dependências: `python-binance`, `pandas` e `ta`

Instale com:

```bash
pip install python-binance pandas ta
```

## Configuração

O arquivo `pro_trading_bot.py` já contém as chaves de API fornecidas neste
exemplo. Caso queira mantê-las fora do código, você pode sobrescrevê-las
definindo as variáveis de ambiente abaixo:

```bash
export BINANCE_KEY="sua_chave"
export BINANCE_SECRET="seu_segredo"
```

**Nunca compartilhe suas chaves de API.** Elas permitem acesso total à sua conta.

## Execução

Basta rodar o script:

```bash
python pro_trading_bot.py
```

O robô buscará os dados recentes, analisará os indicadores e enviará
ordens de compra ou venda de acordo com as regras implementadas.

## Passo a Passo para deixar o robô rodando

1. Instale as dependências listadas na seção **Requisitos**. Caso prefira,
   crie um ambiente virtual para isolar os pacotes:

   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install python-binance pandas ta
   ```

2. (Opcional) Defina suas próprias chaves de API via variáveis de ambiente
   se não quiser utilizar as que acompanham o exemplo:

   ```bash
   export BINANCE_KEY="sua_chave"
   export BINANCE_SECRET="seu_segredo"
   ```

3. Execute o script principal:

   ```bash
   python pro_trading_bot.py
   ```

4. O robô iniciará o loop principal e passará a analisar o mercado a cada
   minuto, enviando ordens de compra ou venda conforme os sinais gerados.

## Aviso
Este código é apenas um exemplo educacional. Negociar ativos digitais é
arriscado e não há garantia de lucro. Utilize por sua conta e risco.
