import json
from uuid import uuid4

from app.models import InvocationRequest
from app.agent.graph import run_agent


async def stream_agent_response(payload: InvocationRequest):
    run_id = str(uuid4())
    query = payload.input.query
    ticker_default = payload.config.ticker_default

    yield {
        "event": "metadata",
        "data": json.dumps({"run_id": run_id, "status": "started"}),
    }

    yield {
        "event": "step",
        "data": json.dumps({"message": "Analyzing user query"}),
    }

    result = await run_agent(query=query, ticker_default=ticker_default)

    for tool_call in result["tool_calls"]:
        yield {
            "event": "tool_result",
            "data": json.dumps(tool_call),
        }

    for source in result["sources"]:
        yield {
            "event": "retrieval_result",
            "data": json.dumps(source),
        }

    answer_text = result["answer"]
    chunk_size = 120
    for i in range(0, len(answer_text), chunk_size):
        yield {
            "event": "token",
            "data": json.dumps({"text": answer_text[i:i + chunk_size]}),
        }

    yield {
        "event": "final",
        "data": json.dumps(
            {
                "answer": result["answer"],
                "sources": result["sources"],
                "tool_calls": result["tool_calls"],
            }
        ),
    }