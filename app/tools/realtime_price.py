from datetime import datetime, timezone
import yfinance as yf


def retrieve_realtime_stock_price(ticker: str) -> dict:
    ticker = ticker.upper().strip()
    stock = yf.Ticker(ticker)

    price = None
    currency = "USD"

    try:
        fast_info = stock.fast_info
        if fast_info:
            price = (
                fast_info.get("lastPrice")
                or fast_info.get("regularMarketPrice")
                or fast_info.get("previousClose")
            )
            currency = fast_info.get("currency", "USD")
    except Exception:
        fast_info = None

    if price is None:
        hist = stock.history(period="1d", interval="1m")
        if hist.empty:
            hist = stock.history(period="5d", interval="1d")
        if hist.empty:
            raise ValueError(f"No market data available for ticker {ticker}")
        price = float(hist["Close"].dropna().iloc[-1])

    return {
        "ticker": ticker,
        "price": float(price),
        "currency": currency,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source": "yfinance",
    }