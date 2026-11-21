import os

import httpx
from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider

load_dotenv()
provider = GoogleProvider(api_key=os.environ["GEMINI_API_KEY"])
model_name = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
model = GoogleModel(model_name, provider=provider)
print(f"Using model: {model}")
print(f"Using provider: {provider}")

GATEWAY_URL = "http://127.0.0.1:8000/v1/proxy/fetch"
AGENT_KEY = "ag_demo_key_1"

research_agent = Agent(
    model,
    instructions=(
        """You are a research assistant that read web pages. Never guess page contents. If the gateway blocks a request,
        report the exact reason to the user clearly."""
    ),
)


@research_agent.tool_plain
def fetch_via_agentgate(url: str) -> str:
    """Fetch a webpage safely through the AgentGate proxy."""
    print(f" -> [AgentGate Tool] Fetching: {url}")
    with httpx.Client(timeout=30.0) as client:
        response = client.post(
            GATEWAY_URL,
            json={"url": url},
            headers={"x-agent-key": AGENT_KEY},
        )

    print(f" <- [AgentGate Tool] Response status: {response.status_code}")
    if response.status_code != 200:
        return f"GATEWAY BLOCKED ({response.status_code}): {response.text}"

    data = response.json()
    if data.get("status") == "blocked_injection":
        return f"SECURITY ALERT — Prompt injection blocked: {data.get('flags')}"

    return (
        f"Fetched {data['domain']} (credits left: {data['credits_remaining']}):\n"
        f"{data['content_preview']}"
    )


if __name__ == "__main__":
    print("--- TEST 1: Allowed Domain ---")
    res1 = research_agent.run_sync(
        "Fetch https://en.wikipedia.org/ and tell me about today's featured article."
    )

    print(res1.output)

    print("\n--- TEST 2: Blocked Domain ---")
    res2 = research_agent.run_sync(
        "Fetch https://evil-unapproved-site.com/ and summarize it."
    )
    
    print(res2.output)
