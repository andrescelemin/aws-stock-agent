import yfinance as yf


def retrieve_historical_stock_price(
    ticker: str,
    start_date: str,
    end_date: str,
    interval: str = "1d",
) -> dict:
    ticker = ticker.upper().strip()
    stock = yf.Ticker(ticker)
    hist = stock.history(start=start_date, end=end_date, interval=interval)

    if hist.empty:
        raise ValueError(
            f"No historical data available for ticker={ticker}, "
            f"start={start_date}, end={end_date}, interval={interval}"
        )

    prices = []
    closes = []

    for idx, row in hist.iterrows():
        close_price = float(row["Close"])
        closes.append(close_price)
        prices.append(
            {
                "date": idx.isoformat(),
                "open": float(row["Open"]),
                "high": float(row["High"]),
                "low": float(row["Low"]),
                "close": close_price,
                "volume": float(row["Volume"]),
            }
        )

    first_close = closes[0]
    last_close = closes[-1]
    period_return_pct = ((last_close - first_close) / first_close) * 100 if first_close else 0.0

    return {
        "ticker": ticker,
        "start_date": start_date,
        "end_date": end_date,
        "interval": interval,
        "prices": prices,
        "summary": {
            "period_high": max(closes),
            "period_low": min(closes),
            "average_close": sum(closes) / len(closes),
            "first_close": first_close,
            "last_close": last_close,
            "period_return_pct": period_return_pct,
        },
        "source": "yfinance",
    }