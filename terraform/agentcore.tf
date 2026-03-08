# AgentCore Runtime resource will be added after:
# 1. container image is built and pushed to ECR
# 2. runtime execution settings are finalized
# 3. inbound auth integration with Cognito is wired in

# Planned resource:
# resource "aws_bedrockagentcore_agent_runtime" "this" { ... }