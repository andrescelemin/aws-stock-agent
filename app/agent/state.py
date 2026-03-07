from typing import Any, TypedDict


class AgentState(TypedDict):
    query: str
    user_id: str | None
    session_id: str | None
    ticker: str | None
    tool_results: list[dict[str, Any]]
    retrieved_context: list[dict[str, Any]]
    final_answer: str | None