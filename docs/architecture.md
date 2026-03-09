\# Architecture Overview



\## Purpose



AWS Stock Agent is a lightweight service designed to demonstrate an AI-ready runtime capable of receiving requests, processing financial queries, and returning structured responses through an API.



The current implementation is a pilot delivery intended to validate architecture, integration flow, and deployment readiness.



---



\## High-Level Components



\### 1. FastAPI Runtime



The application is exposed through a FastAPI service defined in `app/main.py`.



Main endpoints:



\- `GET /health` for health checks

\- `POST /invocations` for runtime requests



---



\### 2. Runtime Agent Layer



The runtime flow is handled through `app/runtime\_agent.py`.



This layer receives the validated request payload and delegates execution to the internal agent logic.



---



\### 3. Agent Graph



The orchestration logic lives under `app/agent/`.



This layer is responsible for structuring the internal execution flow and coordinating reasoning, tools, and retrieval components.



---



\### 4. Tools Layer



The tools live under `app/tools/`.



Current tools include capabilities for:



\- real-time price retrieval

\- historical price retrieval



These tools provide the market-data functionality of the pilot.



---



\### 5. Retrieval Layer



The retrieval components live under `app/retrieval/`.



This layer is intended to access local supporting documents and provide contextual grounding for future agent responses.



---



\### 6. Configuration Layer



Application settings are managed through `app/config.py`.



The service currently depends on environment variables, including the OpenAI API key required at startup.



---



\## Request Flow



1\. A client sends a request to `POST /invocations`

2\. FastAPI validates the request schema

3\. The runtime layer receives the request

4\. The agent orchestration layer processes the request

5\. Tools and retrieval components are used as needed

6\. A structured response is returned to the client



---



\## Deployment Readiness



The repository includes deployment-oriented assets such as:



\- `Dockerfile`

\- `terraform/`

\- environment variable template files



These components show that the project is structured for cloud deployment, even though this delivery is focused on pilot scope rather than full production hardening.



---



\## Current Pilot Scope



This delivery demonstrates:



\- structured repository organization

\- API runtime setup

\- health endpoint validation

\- agent-oriented architecture

\- deployment scaffolding



---



\## Next Steps



Future improvements may include:



\- stronger error handling

\- production-grade authentication

\- full cloud deployment

\- richer document retrieval

\- deeper LLM-based reasoning

\- end-to-end invocation examples

