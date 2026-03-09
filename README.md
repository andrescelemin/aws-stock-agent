# AWS Stock Agent

## Overview

AWS Stock Agent is a lightweight AI-ready microservice designed to demonstrate how an intelligent agent can retrieve financial market data and contextual information from documents.

The project provides a minimal yet structured architecture suitable for deploying AI-powered services using modern cloud infrastructure.

The goal of this project is to demonstrate:

* Building a simple agent-style API
* Retrieving real-time and historical stock market data
* Integrating external data sources
* Preparing the service for cloud deployment using Terraform and Docker

This repository serves as a **technical demonstration of architecture, integration, and deployment readiness**, rather than a fully production-hardened system.

---

# Core Features

### Stock Data Retrieval

The service can retrieve:

* Current stock price
* Historical stock data
* Basic market information

Data is retrieved using the `yfinance` library.

---

### Document Context Retrieval

The project includes a small knowledge base of documents related to Amazon's business and financial strategy.

These documents can be used to provide contextual responses when building more advanced AI agents.

---

### API Endpoints

The service exposes a minimal FastAPI application.

**GET /ping**

Health check endpoint.

Example response:

```
{
  "status": "ok"
}
```

---

**POST /invocations**

Primary endpoint intended to receive agent requests.

Example request:

```
{
  "message": "What is the current price of Amazon stock?"
}
```

Example response:

```
{
  "symbol": "AMZN",
  "price": 178.42
}
```

---

# Project Structure

```
aws-stock-agent
│
├── app/                # FastAPI application
├── data/               # Local documents and resources
│   └── docs/           # Amazon related PDFs
│
├── notebooks/          # Acceptance and demo notebooks
│
├── scripts/            # Utility scripts
│
├── terraform/          # Infrastructure configuration
│
├── Dockerfile          # Container configuration
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
└── README.md
```

---

# Running the Project Locally

## 1 Install dependencies

```
pip install -r requirements.txt
```

---

## 2 Run the API

```
uvicorn app.main:app --reload
```

---

## 3 Test the API

Health check:

```
http://localhost:8000/ping
```

Example POST request:

```
POST http://localhost:8000/invocations
```

Payload example:

```
{
  "message": "What is the current price of Amazon stock?"
}
```

---

# Notebook Demonstration

The repository includes a notebook located in:

```
notebooks/
```

The notebook demonstrates:

* how to invoke the agent
* how payloads are structured
* example outputs

---

# Infrastructure

The project contains a Terraform scaffold intended for cloud deployment.

Infrastructure components may include:

* API hosting
* container deployment
* cloud configuration

Terraform files are located in:

```
terraform/
```

---

# Future Improvements

Possible next steps include:

* integrating LLM reasoning
* implementing vector search
* improving document retrieval
* adding authentication
* deploying to AWS production infrastructure

---

# Quick Test

Run the service locally:

```bash
pip install -r requirements.txt
$env:OPENAI_API_KEY="test-key"
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000

---

# Author

Andrés Celemin Cardoso

AI Engineer | Automation & Intelligent Systems


