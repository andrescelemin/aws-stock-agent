import json
from uuid import uuid4

from app.models import InvocationRequest
from app.agent.graph import compiled_graph


async def stream_agent_response(payload: InvocationRequest):
    run_id = str(uuid4())

    initial_state = {
        "query": payload.input.query,
        "user_id": payload.input.user_id,
        "session_id": payload.input.session_id,
    }

    yield {
        "event": "metadata",
        "data": json.dumps({"run_id": run_id, "status": "started"}),
    }

    try:
        async for chunk in compiled_graph.astream(initial_state, stream_mode="updates"):
            for node_name, node_output in chunk.items():
                yield {
                    "event": "step",
                    "data": json.dumps(
                        {
                            "run_id": run_id,
                            "node": node_name,
                            "output": node_output,
                        },
                        default=str,
                    ),
                }

        final_state = await compiled_graph.ainvoke(initial_state)

        for tool_call in final_state.get("tool_calls", []):
            yield {
                "event": "tool_result",
                "data": json.dumps(tool_call, default=str),
            }

        for source in final_state.get("sources", []):
            yield {
                "event": "retrieval_result",
                "data": json.dumps(source, default=str),
            }

        answer_text = final_state.get("answer", "")
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
                    "answer": final_state.get("answer"),
                    "sources": final_state.get("sources", []),
                    "tool_calls": final_state.get("tool_calls", []),
                    "intent": final_state.get("intent"),
                },
                default=str,
            ),
        }

    except Exception as e:
        yield {
            "event": "error",
            "data": json.dumps(
                {
                    "run_id": run_id,
                    "error": str(e),
                    "type": e.__class__.__name__,
                }
            ),
        }