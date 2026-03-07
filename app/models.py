from typing import Any
from pydantic import BaseModel, Field


class InvocationInput(BaseModel):
    query: str = Field(..., min_length=1)
    user_id: str | None = None
    session_id: str | None = None


class InvocationConfig(BaseModel):
    stream_mode: str = "updates"
    include_sources: bool = True
    ticker_default: str = "AMZN"


class InvocationRequest(BaseModel):
    input: InvocationInput
    config: InvocationConfig = InvocationConfig()


class SourceItem(BaseModel):
    source: str
    page: int | None = None
    excerpt: str | None = None


class FinalResponse(BaseModel):
    answer: str
    sources: list[SourceItem] = []
    tool_calls: list[dict[str, Any]] = []
