import logging
import os
import time

from fastapi import FastAPI, Header, HTTPException

from app.schemas import InvocationRequest, InvocationResponse
from app.runtime_agent import run_agent

app = FastAPI(title="AWS Stock Agent Runtime", version="1.0.0")

logger = logging.getLogger("aws_stock_agent")
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s %(levelname)s %(name)s %(message)s"
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/invocations", response_model=InvocationResponse)
async def invocations(
    payload: InvocationRequest,
    x_amzn_bedrock_agentcore_runtime_session_id: str | None = Header(default=None)
):
    start = time.time()
    session_id = payload.session_id or x_amzn_bedrock_agentcore_runtime_session_id

    try:
        logger.info(
            f"start invocation session_id={session_id} user_id={payload.user_id} message={payload.message}"
        )

        reply = await run_agent(payload)

        elapsed = round(time.time() - start, 3)
        logger.info(f"success invocation session_id={session_id} elapsed={elapsed}s")

        return InvocationResponse(
            reply=reply,
            session_id=session_id,
            status="ok"
        )

    except Exception:
        elapsed = round(time.time() - start, 3)
        logger.exception(f"failed invocation session_id={session_id} elapsed={elapsed}s")
        raise HTTPException(status_code=500, detail="Internal error")
