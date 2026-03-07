from fastapi import APIRouter
from sse_starlette.sse import EventSourceResponse

from app.models import InvocationRequest
from app.agent.streaming import stream_agent_response

router = APIRouter()


@router.get("/ping")
async def ping():
    return {"status": "ok"}


@router.post("/invocations")
async def invoke(payload: InvocationRequest):
    return EventSourceResponse(stream_agent_response(payload))