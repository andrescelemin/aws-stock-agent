from app.schemas import InvocationRequest
from app.agent.graph import compiled_graph


async def run_agent(request: InvocationRequest) -> str:
    user_message = request.message.strip()

    if not user_message:
        return "No recibí ningún mensaje."

    result = await compiled_graph.ainvoke({
        "query": user_message
    })

    if isinstance(result, dict):
        answer = result.get("answer")
        if answer:
            return str(answer)

    return str(result)
