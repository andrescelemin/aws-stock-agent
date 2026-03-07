from datetime import date

from langchain_openai import ChatOpenAI

from app.config import settings
from app.agent.prompts import SYSTEM_PROMPT
from app.tools.realtime_price import retrieve_realtime_stock_price
from app.tools.historical_price import retrieve_historical_stock_price
from app.retrieval.retriever import retrieve_relevant_chunks


llm = ChatOpenAI(
    model=settings.openai_model,
    api_key=settings.openai_api_key,
    temperature=0.1,
)


def infer_ticker(query: str, default_ticker: str = "AMZN") -> str:
    query_upper = query.upper()
    if "AMZN" in query_upper or "AMAZON" in query_upper:
        return "AMZN"
    return default_ticker


def looks_like_historical_query(query: str) -> bool:
    q = query.lower()
    signals = [
        "historical",
        "q4",
        "q3",
        "q2",
        "last year",
        "in 2024",
        "in 2025",
        "were the stock prices",
    ]
    return any(signal in q for signal in signals)


def build_historical_range_from_query(query: str) -> tuple[str, str]:
    q = query.lower()
    current_year = date.today().year
    last_year = current_year - 1

    if "q4 last year" in q:
        return f"{last_year}-10-01", f"{last_year}-12-31"

    return f"{last_year}-01-01", f"{last_year}-12-31"


async def run_agent(query: str, ticker_default: str = "AMZN") -> dict:
    ticker = infer_ticker(query, ticker_default)
    tool_calls = []
    sources = []
    retrieval_context = []
    market_result = None

    if looks_like_historical_query(query):
        start_date, end_date = build_historical_range_from_query(query)
        market_result = retrieve_historical_stock_price(
            ticker=ticker,
            start_date=start_date,
            end_date=end_date,
            interval="1d",
        )
        tool_calls.append({"tool": "retrieve_historical_stock_price", "ticker": ticker})
    else:
        market_result = retrieve_realtime_stock_price(ticker=ticker)
        tool_calls.append({"tool": "retrieve_realtime_stock_price", "ticker": ticker})

    retrieval_context = retrieve_relevant_chunks(query, top_k=3)
    for item in retrieval_context:
        sources.append(
            {
                "source": item["source"],
                "page": item["page"],
                "excerpt": item["text"][:300],
            }
        )

    prompt = f"""
{SYSTEM_PROMPT}

User query:
{query}

Market data:
{market_result}

Retrieved context:
{retrieval_context}
"""

    response = await llm.ainvoke(prompt)

    return {
        "answer": response.content,
        "sources": sources,
        "tool_calls": tool_calls,
        "market_result": market_result,
    }