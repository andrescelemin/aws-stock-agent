from app.schemas import InvocationRequest


def run_agent(request: InvocationRequest) -> str:
    user_message = request.message.strip()

    if not user_message:
        return "No recibí ningún mensaje."

    return f"Procesé tu mensaje correctamente: {user_message}"
