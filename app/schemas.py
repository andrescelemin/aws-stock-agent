from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class InvocationRequest(BaseModel):
    message: str = Field(..., description="Mensaje del usuario")
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class InvocationResponse(BaseModel):
    reply: str
    session_id: Optional[str] = None
    agent: str = "aws_stock_agent"
    status: str = "ok"
