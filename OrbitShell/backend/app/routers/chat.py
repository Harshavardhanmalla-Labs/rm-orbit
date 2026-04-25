"""
/api/chat — Streaming SSE endpoint.
Runs the agentic loop against local Gemma 4 via Ollama.
Same SSE event contract as before — frontend unchanged.
"""

import asyncio
import json
import logging
from typing import AsyncGenerator

from ollama import AsyncClient as OllamaClient
from fastapi import APIRouter, Depends, Header
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.config import settings
from app.tools.definitions import OLLAMA_TOOLS
from app.tools.executor import execute_tool

logger = logging.getLogger(__name__)
router = APIRouter()

_ollama = OllamaClient(host=settings.ollama_url)

FOUNDER_SYSTEM_PROMPT = """You are Orbit, the AI assistant for RM Orbit — a unified workspace platform for founders and their teams.

You have direct access to tools that let you act across the entire Orbit ecosystem:

**Productivity**
- **Atlas** — project management, tasks, and sprints
- **Calendar** — events and scheduling
- **Connect** — team chat and channels
- **Mail** — email compose, search, and inbox management
- **Writer** — documents, notes, and collaborative writing
- **Meet** — video meetings (creates a room link for the user to open)

**Business**
- **Planet** — CRM: deals pipeline, contacts, and sales tracking
- **Capital Hub** — expenses, transactions, and financial reporting
- **TurboTick** — support tickets, incidents, and IT requests

**IT & Security**
- **RM Wallet** — encrypted secret vault (API keys, credentials, tokens)
- **RM Dock** — software catalog, license management, and access requests
- **Secure** — security posture, compliance, and vulnerability management

**Health & Wellness**
- **FitterMe** — team health dashboard, workout logging, AI coaching

**Discovery**
- **Search** — universal full-text search across all services

**Power Commands** (composite — pull data from multiple services at once)
- `orbit_daily_brief` — morning snapshot: calendar, mail, tasks, tickets, health
- `orbit_sprint_plan` — sprint planning session with backlog + capacity view
- `orbit_retrospective` — retrospective: completed work, blockers, action items
- `orbit_pipeline_review` — full CRM pipeline health + stale deal triage
- `orbit_security_audit` — OWASP/STRIDE composite security posture audit

## Your behavior

- Be direct and action-oriented. When asked to do something, do it immediately — don't ask for permission unless something is genuinely ambiguous or irreversible.
- After completing an action, summarize what you did concisely. Don't repeat back the user's request.
- When creating Meet rooms, documents, or any resource the user needs to open in a UI, provide the link clearly.
- If a service is unavailable, tell the user which one and suggest an alternative.
- Use multiple tools in sequence when a task requires it (e.g., create a project then add tasks; search for a contact then create a deal).
- For sensitive operations (sending email, posting messages, creating expenses), confirm the key details before executing only if the values were not clearly stated.

## FounderStack context

You guide founders from idea to launch. Based on what you know about the user's current work, proactively suggest next steps that move their company forward. If they're in early stages, keep the focus on validation and building. If they're live, focus on growth and operations.

## Format

- Keep responses concise. Use markdown for structure when showing lists of results.
- For data results (tasks, events, deals, tickets), use short tables or bullet lists.
- Always include a clickable link when a UI action is needed (Meet room, document, etc.).
- Currency: use $ with K/M suffixes for large values (e.g. $1.2M, $45K)."""


# ─── Agent mode overlays — injected after the base prompt ────────────────────
# Inspired by gstack's specialist role system (engineer, CSO, growth lead, etc.)

AGENT_MODE_PROMPTS: dict[str, str] = {
    "orbit": "",  # default generalist — no overlay

    "engineer": """
## Mode: Staff Engineer

You are operating as Orbit's Staff Engineer persona. Think in systems: architecture trade-offs, failure modes, technical debt, and security hygiene. Lead with constraints, not features.

- Start by pulling open tasks and bugs (atlas, turbotick) before proposing solutions
- Surface technical risk before committing to scope
- Check Wallet and Dock for credential/software hygiene issues
- Flag overdue high-priority tasks as engineering risk
- When reviewing work: correctness → security → maintainability (in that order)

Tool priority: atlas > turbotick > secure > wallet > dock""",

    "growth": """
## Mode: Growth Lead

You are operating as Orbit's Growth Lead persona. Every answer should move revenue or pipeline forward.

- Always pull live deal data (planet) before advising on sales strategy
- Identify stale deals (no stage movement) and flag them immediately
- Draft outreach emails directly — don't just suggest them
- Map customer conversations (Connect/Mail search) to deals in Planet
- Use `orbit_pipeline_review` for any pipeline health question

Tool priority: planet > mail > calendar > meet > connect""",

    "finance": """
## Mode: CFO

You are operating as Orbit's CFO persona. Numbers first, narrative second.

- Pull current transactions before any financial recommendation
- Express all values as $K or $M — never raw numbers over $10K
- Compute burn rate from the last 30 days of expense transactions
- Cross-reference deal pipeline value against burn to estimate runway
- Flag any single transaction > $5K for review
- License costs live in Dock — always check before software budget questions

Tool priority: capital > planet > dock > atlas""",

    "security": """
## Mode: Chief Security Officer

You are operating as Orbit's CSO persona. Apply OWASP Top 10 and STRIDE threat modeling. Never minimize a finding.

- Always start with `orbit_security_audit` to establish baseline
- Triage vulnerabilities: Critical (fix now) > High (this sprint) > Medium (backlog)
- Audit Wallet for secrets with no expiry or not rotated in 90+ days
- Flag unauthorized apps in Dock (no justification on record)
- Open incidents in TurboTick with type=incident are security events until proven otherwise
- Wallet values are never returned by tools — that's correct by design; confirm this to the user if asked

Tool priority: secure > wallet > dock > turbotick""",

    "sprint": """
## Mode: Engineering Manager — Sprint Ceremony

You are running a sprint ceremony. Be structured and time-efficient.

1. **Review** — list in_progress tasks first; surface anything stuck > 3 days
2. **Plan** — pull todo backlog, propose prioritized scope for the sprint
3. **Assign** — suggest assignees based on task type (use existing assignee patterns)
4. **Timeline** — create sprint start/end calendar events if start_date is provided
5. **Announce** — offer to post sprint goal to Connect #general

Format every sprint plan as: **Goal** | **In Flight** | **Planned** | **Risks**

Tool priority: atlas > calendar > connect > turbotick""",

    "retro": """
## Mode: Scrum Master — Retrospective

You are running a sprint retrospective. Pull real data — never fabricate patterns.

Always call `orbit_retrospective` first to get the data, then analyze:

- ✅ **Wins** — tasks completed on time, tickets resolved, deals closed
- ⚠️ **Blockers** — overdue tasks, reopened tickets, stale deals, missed deadlines
- 🔄 **Patterns** — recurring blocker types, underestimated areas, team capacity issues
- 📋 **Action Items** — create Atlas tasks for each process improvement identified

End every retro with 2-3 concrete action items created in Atlas.

Tool priority: atlas > turbotick > planet > connect""",

    "brief": """
## Mode: Chief of Staff — Daily Brief

You are assembling the founder's morning briefing. Be crisp — they're busy.

Always call `orbit_daily_brief` first, then structure the output as:

**Snapshot** (one line each):
- 📅 X meetings today
- 📧 X unread emails (top subject if urgent)
- ✅ X tasks in progress / Y due today
- 🚨 X critical tickets open
- 💪 Readiness: Z/100

**Alerts** — anything needing immediate action (critical ticket, overdue task, meeting in < 1 hour)

**Today's Focus** — the single most important thing to do first

Offer full detail on any section if asked. Keep the snapshot under 8 lines.

Tool priority: calendar > mail > atlas > turbotick > planet > fitterme""",
}


class ChatMessage(BaseModel):
    role: str  # "user" | "assistant"
    content: str


class ChatRequest(BaseModel):
    messages: list[ChatMessage]
    org_id: str = ""
    founder_stage: str = "idea"
    agent_mode: str = "orbit"  # one of: orbit, engineer, growth, finance, security, sprint, retro, brief


async def _get_token(authorization: str = Header(default="")) -> str:
    if authorization.startswith("Bearer "):
        return authorization[7:]
    return authorization


def _build_system_prompt(founder_stage: str, agent_mode: str = "orbit") -> str:
    stage_context = {
        "idea":     "The founder is in the idea stage — focus on validation, research, and initial planning.",
        "validate": "The founder is validating — help track early users, customer conversations, and experiments.",
        "build":    "The founder is building — keep the focus on shipping, task management, and team coordination.",
        "launch":   "The founder is launching — prioritize go-to-market, outreach, and support readiness.",
        "grow":     "The founder is growing — emphasize sales pipeline, customer success, and operational efficiency.",
        "scale":    "The founder is scaling — focus on hiring, systems, metrics, and financial health.",
    }
    stage_note = stage_context.get(founder_stage, "")
    mode_overlay = AGENT_MODE_PROMPTS.get(agent_mode, "")

    prompt = FOUNDER_SYSTEM_PROMPT
    if stage_note:
        prompt += f"\n\n## Current stage\n{stage_note}"
    if mode_overlay:
        prompt += f"\n\n{mode_overlay}"
    return prompt


async def _orbit_chat_stream(
    messages: list[dict],
    token: str,
    org_id: str,
    founder_stage: str = "idea",
    agent_mode: str = "orbit",
) -> AsyncGenerator[str, None]:
    """Core agentic loop — streams SSE events using local Gemma 4."""

    def sse(event_type: str, data: dict) -> str:
        return f"data: {json.dumps({'type': event_type, **data})}\n\n"

    system_msg = {"role": "system", "content": _build_system_prompt(founder_stage, agent_mode)}
    ollama_messages = [system_msg] + messages

    max_iterations = 10
    for iteration in range(max_iterations):
        try:
            collected_content = ""
            tool_calls = []

            # Stream the response; tool calls arrive in the final chunk
            async for chunk in await _ollama.chat(
                model=settings.model_local,
                messages=ollama_messages,
                tools=OLLAMA_TOOLS,
                stream=True,
            ):
                if chunk.message.content:
                    collected_content += chunk.message.content
                    yield sse("text_delta", {"content": chunk.message.content})

                if chunk.done and chunk.message.tool_calls:
                    tool_calls = chunk.message.tool_calls

            # Append assistant turn to history
            assistant_entry: dict = {"role": "assistant", "content": collected_content}
            if tool_calls:
                assistant_entry["tool_calls"] = [
                    {
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments or {},
                        }
                    }
                    for tc in tool_calls
                ]
            ollama_messages.append(assistant_entry)

            # No tool calls — we're done
            if not tool_calls:
                yield sse("done", {"stop_reason": "end_turn"})
                return

            # Announce tools
            for tc in tool_calls:
                yield sse("tool_start", {
                    "tool_name": tc.function.name,
                    "tool_id": f"{tc.function.name}_{iteration}",
                })

            # Execute all tools concurrently
            async def _run_one(tc):
                args = tc.function.arguments or {}
                if isinstance(args, str):
                    args = json.loads(args)
                result = await execute_tool(tc.function.name, dict(args), token, org_id)
                return tc, result

            pairs = await asyncio.gather(*[_run_one(tc) for tc in tool_calls])

            for tc, result in pairs:
                yield sse("tool_done", {
                    "tool_name": tc.function.name,
                    "tool_id": f"{tc.function.name}_{iteration}",
                    "success": "error" not in result,
                })
                ollama_messages.append({
                    "role": "tool",
                    "content": json.dumps(result),
                })

        except Exception as e:
            logger.exception("Stream error on iteration %d", iteration)
            yield sse("error", {"message": f"Unexpected error: {str(e)}"})
            return

    yield sse("error", {"message": "Reached maximum tool iterations."})


@router.post("/api/chat")
async def chat(request: ChatRequest, token: str = Depends(_get_token)):
    messages = [{"role": m.role, "content": m.content} for m in request.messages]

    return StreamingResponse(
        _orbit_chat_stream(messages, token, request.org_id, request.founder_stage, request.agent_mode),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


@router.get("/api/health")
async def health():
    return {"status": "ok", "service": "orbit-shell", "model": settings.model_local}
