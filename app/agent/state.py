from typing import Any, TypedDict


class AgentState(TypedDict, total=False):
    query: str
    user_id: str | None
    session_id: str | None
    ticker: str | None
    intent: str
    start_date: str | None
    end_date: str | None
    market_result: dict[str, Any] | None
    retrieved_context: list[dict[str, Any]]
    sources: list[dict[str, Any]]
    tool_calls: list[dict[str, Any]]
    answer: str | None