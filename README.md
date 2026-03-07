# AWS Stock Agent

AI agent solution on AWS using FastAPI, AgentCore Runtime, Cognito, LangGraph-oriented orchestration, yfinance tools, document retrieval, Langfuse observability, and Terraform infrastructure.

## Project Goal

Build an AI agent hosted on AWS that can answer real-time and historical Amazon stock questions, retrieve relevant information from Amazon investor documents, and stream responses back to the client.

## Current Features

- FastAPI app with:
  - `GET /ping`
  - `POST /invocations`
- Real-time stock retrieval with `yfinance`
- Historical stock retrieval with `yfinance`
- PDF document retrieval over:
  - Amazon 2024 Annual Report
  - Amazon Q3 2025 Earnings Release
  - Amazon Q2 2025 Earnings Release
- SSE-style streaming responses
- Langfuse configuration scaffold
- Terraform folder scaffold for infrastructure

## Project Structure

```text
aws-stock-agent/
├─ app/
├─ data/
├─ notebooks/
├─ scripts/
├─ terraform/
├─ Dockerfile
├─ requirements.txt
├─ .env.example
└─ README.md