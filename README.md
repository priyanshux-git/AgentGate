# AgentGate — Identity, Permissions & Safe-Web Gateway for AI Agents

AgentGate is a FastAPI gateway and MCP server that gives AI agents verifiable identity, scoped permissions, hard spending caps, human-in-the-loop approvals, and a sanitized web-browsing layer that uses Olostep for reliable page extraction and AgentGate's own middleware for prompt-injection defense.

## Project Scope
- **Who it is for:** Developers and teams deploying autonomous AI agents that browse the web, call APIs, or spend money on behalf of users.
- **What it does:** Sits between an AI agent and external tools/websites to enforce identity, budgets, domain rules, prompt-injection filtering, and human approval before high-risk actions execute.

## AI Tools, Models & Libraries Used
- **Backend & Validation:** FastAPI, Pydantic, SQLModel (SQLite)
- **Web Layer for Agents:** Olostep Python SDK
- **Demo Agent & Orchestration:** Pydantic AI, Model Context Protocol (MCP)
- **LLM Models:** Gemini 3.5 Flash Lite / Gemini Flash Lite (via Google AI Studio API)
- **Testing & Evaluation:** Keploy, custom Python red-team eval harness

---

## Getting Started & Setup

### 1. Prerequisites
- **Python**: Version 3.12+ (or 3.14 via `uv`)
- **API Keys**:
  - **Gemini API Key**: Obtain a free key from [Google AI Studio](https://aistudio.google.com/).
  - **Olostep API Key**: Obtain an API key from [Olostep](https://olostep.com/) for reliable web extraction.

---

### 2. Setup

Clone the repository and navigate into the project directory:

```bash
git clone https://github.com/priyanshux-git/agent_gate.git
cd agent_gate
```

#### Option A: Using `uv` (Recommended)
```bash
uv sync
```

#### Option B: Using standard Python `venv` and `pip`
```bash
python -m venv .venv

# On Windows (PowerShell):
.venv\Scripts\Activate.ps1
# On Linux/macOS:
source .venv/bin/activate

pip install "fastapi[standard]>=0.165.0" "olostep>=1.2.3" "pydantic-ai>=2.71.0" python-dotenv httpx
```

---

### 3. Environment Configuration

Copy the example `.env` file and configure your credentials:

```bash
cp .env.example .env
```

Update `.env` with your API keys:

```env
OLOSTEP_API_KEY=your_olostep_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

---

### 4. Running the Project

#### Step 1: Start the FastAPI Gateway Server
In your first terminal, launch the gateway:

```bash
# Using uv:
uv run fastapi dev

# Or with virtual environment activated:
fastapi dev
```

- **Gateway URL**: `http://127.0.0.1:8000`
- **Interactive Swagger Docs**: `http://127.0.0.1:8000/docs`
- **Proxy Endpoint**: `POST /v1/proxy/fetch`

#### Step 2: Run the Demo Research Agent
In a separate terminal, run the Pydantic AI research agent test script:

```bash
# Using uv:
uv run python agent_test.py

# Or with virtual environment activated:
python agent_test.py
```

This runs two test cases:
1. **TEST 1 (Allowed Domain)**: The agent routes a request through AgentGate to scrape `https://books.toscrape.com/` and extracts the first two book titles.
2. **TEST 2 (Blocked Domain)**: The agent attempts to access an unapproved domain (`https://evil-unapproved-site.com/`), which is rejected by the gateway with HTTP 403 Forbidden.
