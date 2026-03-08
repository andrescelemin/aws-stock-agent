output "aws_region" {
  value = var.aws_region
}

output "cognito_user_pool_id" {
  value = aws_cognito_user_pool.this.id
}

output "cognito_user_pool_arn" {
  value = aws_cognito_user_pool.this.arn
}

output "cognito_user_pool_client_id" {
  value = aws_cognito_user_pool_client.this.id
}

output "cognito_user_pool_client_secret" {
  value     = aws_cognito_user_pool_client.this.client_secret
  sensitive = true
}

output "cognito_domain" {
  value = aws_cognito_user_pool_domain.this.domain
}

output "ecr_repository_name" {
  value = aws_ecr_repository.agent.name
}

output "ecr_repository_url" {
  value = aws_ecr_repository.agent.repository_url
}

output "agent_runtime_role_arn" {
  value = aws_iam_role.agent_runtime.arn
}