from datetime import date
from typing import Literal

from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI

from app.config import settings
from app.agent.state import AgentState
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


def classify_intent(query: str) -> str:
    q = query.lower()

    if any(x in q for x in ["stock price right now", "current price", "right now"]):
        if any(y in q for y in ["ai business", "relevant information", "report"]):
            return "hybrid"
        return "realtime"

    if any(x in q for x in ["historical", "q4", "q3", "q2", "last year", "stock prices"]):
        if any(y in q for y in ["predicted", "analysts", "report", "earnings"]):
            return "hybrid"
        return "historical"

    if any(x in q for x in ["office space", "north america", "annual report", "ai business", "analysts", "predicted"]):
        return "document"

    if any(x in q for x in ["relevant information", "researching amzn"]):
        return "hybrid"

    return "realtime"


def build_historical_range_from_query(query: str) -> tuple[str, str]:
    q = query.lower()
    current_year = date.today().year
    last_year = current_year - 1

    if "q4 last year" in q:
        return f"{last_year}-10-01", f"{last_year}-12-31"
    if "q3 last year" in q:
        return f"{last_year}-07-01", f"{last_year}-09-30"
    if "q2 last year" in q:
        return f"{last_year}-04-01", f"{last_year}-06-30"
    if "q1 last year" in q:
        return f"{last_year}-01-01", f"{last_year}-03-31"

    return f"{last_year}-01-01", f"{last_year}-12-31"


def initialize_state(state: AgentState) -> AgentState:
    query = state["query"]
    ticker = infer_ticker(query, settings.default_ticker)
    intent = classify_intent(query)

    new_state: AgentState = {
        **state,
        "ticker": ticker,
        "intent": intent,
        "tool_calls": [],
        "sources": [],
        "retrieved_context": [],
        "market_result": None,
        "answer": None,
    }

    if intent == "historical" or intent == "hybrid":
        start_date, end_date = build_historical_range_from_query(query)
        new_state["start_date"] = start_date
        new_state["end_date"] = end_date

    return new_state


def realtime_node(state: AgentState) -> AgentState:
    market_result = retrieve_realtime_stock_price(state["ticker"])
    tool_calls = state.get("tool_calls", [])
    tool_calls.append({"tool": "retrieve_realtime_stock_price", "ticker": state["ticker"]})

    return {
        **state,
        "market_result": market_result,
        "tool_calls": tool_calls,
    }


def historical_node(state: AgentState) -> AgentState:
    market_result = retrieve_historical_stock_price(
        ticker=state["ticker"],
        start_date=state["start_date"],
        end_date=state["end_date"],
        interval="1d",
    )
    tool_calls = state.get("tool_calls", [])
    tool_calls.append(
        {
            "tool": "retrieve_historical_stock_price",
            "ticker": state["ticker"],
            "start_date": state["start_date"],
            "end_date": state["end_date"],
        }
    )

    return {
        **state,
        "market_result": market_result,
        "tool_calls": tool_calls,
    }


def retrieval_node(state: AgentState) -> AgentState:
    chunks = retrieve_relevant_chunks(state["query"], top_k=3)
    sources = []

    for item in chunks:
        sources.append(
            {
                "source": item["source"],
                "page": item["page"],
                "excerpt": item["text"][:300],
            }
        )

    return {
        **state,
        "retrieved_context": chunks,
        "sources": sources,
    }


async def synthesize_node(state: AgentState) -> AgentState:
    prompt = f"""
{SYSTEM_PROMPT}

User query:
{state["query"]}

Intent:
{state["intent"]}

Market data:
{state.get("market_result")}

Retrieved context:
{state.get("retrieved_context", [])}
"""

    response = await llm.ainvoke(prompt)

    return {
        **state,
        "answer": response.content,
    }


def route_after_initialize(state: AgentState) -> Literal["realtime", "historical", "document", "hybrid"]:
    return state["intent"]


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("initialize", initialize_state)
    graph.add_node("realtime", realtime_node)
    graph.add_node("historical", historical_node)
    graph.add_node("document", retrieval_node)
    graph.add_node("hybrid_retrieval", retrieval_node)
    graph.add_node("synthesize", synthesize_node)

    graph.set_entry_point("initialize")

    graph.add_conditional_edges(
        "initialize",
        route_after_initialize,
        {
            "realtime": "realtime",
            "historical": "historical",
            "document": "document",
            "hybrid": "historical",
        },
    )

    graph.add_edge("realtime", "synthesize")
    graph.add_edge("historical", "hybrid_retrieval")
    graph.add_edge("document", "synthesize")
    graph.add_edge("hybrid_retrieval", "synthesize")
    graph.add_edge("synthesize", END)

    return graph.compile()


compiled_graph = build_graph()