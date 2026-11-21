from typing import Annotated
from urllib.parse import urlparse

from fastapi import APIRouter, Depends, Header, HTTPException, status
from olostep import AsyncOlostep, ScrapeResult
from pydantic import BaseModel

from olostep_dep import get_olostep

test = APIRouter()

# only for testing, sqlite will be use4d
AGENTS = {
    "ag_demo_key_1": {
        "agent_id": "research-bot-01",
        "owner": "priyanshu",
        "allowed_domains": ["books.toscrape.com", "en.wikipedia.org", "example.com"],
        "credit_limit": 50,
        "credits_used": 0,
    },
    "ag_demo_key_2": {
        "agent_id": "research-bot-02",
        "owner": "priyanshu",
        "allowed_domains": ["en.wikipedia.org", "example.com"],
        "credit_limit": 20,
        "credits_used": 0,
    },
}

# only for testing. AI will be used for prompt injection protection
INJECTION_PATTERNS = [
    "ignore previous instructions",
    "disregard all prior instructions",
    "system prompt",
    "transfer funds immediately",
]


class AgentKey(BaseModel):
    x_agent_key: str


class FetchRequest(BaseModel):
    url: str | None = None


@test.post("/v1/proxy/fetch")
async def safe_web_fetch(
    agent_key: Annotated[AgentKey, Header()],
    olostep: Annotated[AsyncOlostep, Depends(get_olostep)],
    body: FetchRequest | None = None,
):
    target_url = (body.url if body and body.url else None)
    if not target_url:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Field 'url' is required in JSON body or query parameter.",
        )
    url = target_url
    agent = AGENTS.get(agent_key.x_agent_key)

    if not agent:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Agent Passport key.",
        )

    domain = urlparse(url).netloc.lower()

    if domain not in agent["allowed_domains"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Blocked: domain '{domain}' is not in {agent['agent_id']}'s allowlist.",
        )

    if agent["credits_used"] >= agent["credit_limit"]:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="Blocked: Agent credit budget exhausted.",
        )

    scrape: ScrapeResult = await olostep.scrapes.create(
        url_to_scrape=url,
        formats=["markdown"],
    )

    markdown: str = getattr(scrape, "markdown_content", None) or ""

    print("markdown :", markdown)

    cost: int = getattr(scrape, "credits_consumed", None) or 1

    agent["credits_used"] += cost

    lowered = markdown.lower()
    flagged = [p for p in INJECTION_PATTERNS if p in lowered]
    if flagged:
        return {
            "status": "blocked_injection",
            "agent_id": agent["agent_id"],
            "flags": flagged,
            "credits_remaining": agent["credit_limit"] - agent["credits_used"],
        }

    return {
        "status": "allowed",
        "agent_id": agent["agent_id"],
        "domain": domain,
        "credits_used_this_call": cost,
        "credits_remaining": agent["credit_limit"] - agent["credits_used"],
        "content_preview": markdown[:4500],
    }
