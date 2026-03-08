resource "aws_bedrockagentcore_agent_runtime" "this" {
  agent_runtime_name = "aws_stock_agent_dev_runtime"
  role_arn           = aws_iam_role.agent_runtime.arn

  environment_variables = {
    OPENAI_API_KEY = var.openai_api_key
  }

  agent_runtime_artifact {
    container_configuration {
      container_uri = "${aws_ecr_repository.agent.repository_url}:latest"
    }
  }

  network_configuration {
    network_mode = "PUBLIC"
  }

  protocol_configuration {
    server_protocol = "HTTP"
  }

  lifecycle_configuration {
    max_lifetime                 = 600
    idle_runtime_session_timeout = 600
  }

  depends_on = [aws_ecr_repository.agent]
}