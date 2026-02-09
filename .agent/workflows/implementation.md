---
description: CodeSentinel Implementation Workflow
---

# CodeSentinel Implementation Workflow

Follow these steps to build out the project systematically.

## 1. Setup Backend Environment
- Create a `backend` directory.
- Initialize `venv` or `poetry`.
- Install `fastapi`, `uvicorn`, `docker`, `langchain-google-genai`, `langgraph`.

## 2. Implement Sandbox (Docker)
- Define a `docker-compose.yml` for development.
- Create `backend/app/core/sandbox.py`.
- Test command execution inside a container.

## 3. Implement AST Parsing
- Create `backend/app/utils/ast_parser.py` using `tree-sitter`.
- Test parsing a sample repository.

## 4. Construct LangGraph Brain
- Define the node functions (Plan, Edit, Test, Verify).
- Connect them with conditional edges based on test results.

## 5. UI Implementation
- Update `App.tsx` and components to connect to the backend via WebSockets.
- Implement the `Terminal` component to show real-time agent output.

// turbo-all
## 6. Execution & Testing
- Run `npm run dev` for frontend.
- Run `uvicorn app.main:app` for backend.
