variable "aws_region" {
  description = "AWS region for deployment"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Project name prefix"
  type        = string
  default     = "aws-stock-agent"
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "dev"
}

variable "cognito_callback_urls" {
  description = "Allowed callback URLs for Cognito app client"
  type        = list(string)
  default = [
    "http://localhost:3000/callback",
    "http://localhost:8080/callback"
  ]
}

variable "cognito_logout_urls" {
  description = "Allowed logout URLs for Cognito app client"
  type        = list(string)
  default = [
    "http://localhost:3000/logout",
    "http://localhost:8080/logout"
  ]
}

variable "openai_api_key" {
  description = "OpenAI API key for runtime"
  type        = string
  sensitive   = true
}