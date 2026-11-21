# AgentGate — Identity, Permissions & Safe-Web Gateway for AI Agents

AgentGate is a FastAPI gateway and MCP server that gives AI agents verifiable identity, scoped permissions, hard spending caps, human-in-the-loop approvals, and a sanitized web-browsing layer that uses Olostep for reliable page extraction and AgentGate's own middleware for prompt-injection defense.

## Project Scope
- **Who it is for:** Developers and teams deploying autonomous AI agents that browse the web, call APIs, or spend money on behalf of users.
- **What it does:** Sits between an AI agent and external tools/websites to enforce identity, budgets, domain rules, prompt-injection filtering, and human approval before high-risk actions execute.

## AI Tools, Models & Libraries Used
- **Backend & Validation:** FastAPI, Pydantic, SQLModel (SQLite)
- **Web Layer for Agents:** Olostep Python SDK
- **Demo Agent & Orchestration:** Pydantic AI, Model Context Protocol (MCP)
- **LLM Models:** Gemini 3.8 Flash (via Google AI Studio API)
- **Testing & Evaluation:** Keploy, custom Python red-team eval harness
