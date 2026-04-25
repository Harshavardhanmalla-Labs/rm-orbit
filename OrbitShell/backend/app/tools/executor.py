"""
Tool executor — translates Claude tool calls into HTTP requests to RM Orbit services.
Each function maps a tool name + inputs → HTTP call → normalized result.
"""

import asyncio
import httpx
import logging
from datetime import date, timedelta
from typing import Any
from app.config import settings

logger = logging.getLogger(__name__)

# Shared async HTTP client (reused across requests)
_client: httpx.AsyncClient | None = None


def get_http_client() -> httpx.AsyncClient:
    global _client
    if _client is None or _client.is_closed:
        _client = httpx.AsyncClient(timeout=15.0)
    return _client


def _auth_headers(token: str, org_id: str) -> dict:
    return {
        "Authorization": f"Bearer {token}",
        "X-Org-Id": org_id,
        "Content-Type": "application/json",
    }


async def execute_tool(tool_name: str, tool_input: dict, token: str, org_id: str) -> Any:
    """Route a tool call to the appropriate service and return the result."""
    client = get_http_client()
    headers = _auth_headers(token, org_id)

    try:
        if tool_name.startswith("atlas_"):
            return await _atlas(client, headers, tool_name, tool_input)
        elif tool_name.startswith("calendar_"):
            return await _calendar(client, headers, tool_name, tool_input)
        elif tool_name.startswith("connect_"):
            return await _connect(client, headers, tool_name, tool_input)
        elif tool_name.startswith("mail_"):
            return await _mail(client, headers, tool_name, tool_input)
        elif tool_name.startswith("writer_"):
            return await _writer(client, headers, tool_name, tool_input)
        elif tool_name.startswith("planet_"):
            return await _planet(client, headers, tool_name, tool_input)
        elif tool_name.startswith("turbotick_"):
            return await _turbotick(client, headers, tool_name, tool_input)
        elif tool_name == "orbit_search":
            return await _search(client, headers, tool_input)
        elif tool_name.startswith("capital_"):
            return await _capital(client, headers, tool_name, tool_input)
        elif tool_name == "meet_create_room":
            return await _meet(client, headers, tool_input)
        elif tool_name == "meet_get_pre_call_brief":
            return await _meet_pre_call_brief(client, headers, tool_input)
        elif tool_name == "meet_post_call_sync":
            return await _meet_post_call_sync(client, headers, tool_input)
        elif tool_name.startswith("wallet_"):
            return await _wallet(client, headers, tool_name, tool_input)
        elif tool_name.startswith("dock_"):
            return await _dock(client, headers, tool_name, tool_input)
        elif tool_name.startswith("fitterme_"):
            return await _fitterme(client, headers, tool_name, tool_input)
        elif tool_name.startswith("secure_"):
            return await _secure(client, headers, tool_name, tool_input)
        elif tool_name == "orbit_daily_brief":
            return await _orbit_daily_brief(client, headers, tool_input)
        elif tool_name == "orbit_sprint_plan":
            return await _orbit_sprint_plan(client, headers, tool_input)
        elif tool_name == "orbit_retrospective":
            return await _orbit_retrospective(client, headers, tool_input)
        elif tool_name == "orbit_pipeline_review":
            return await _orbit_pipeline_review(client, headers, tool_input)
        elif tool_name == "orbit_security_audit":
            return await _orbit_security_audit(client, headers, tool_input)
        else:
            return {"error": f"Unknown tool: {tool_name}"}
    except httpx.ConnectError as e:
        svc = tool_name.split("_")[0]
        return {"error": f"{svc} service is not reachable. It may be offline.", "detail": str(e)}
    except httpx.TimeoutException:
        return {"error": f"Request to service timed out for tool {tool_name}"}
    except Exception as e:
        logger.exception(f"Tool execution failed: {tool_name}")
        return {"error": str(e)}


# ─── ATLAS ────────────────────────────────────────────────────────────────────

async def _atlas(client: httpx.AsyncClient, headers: dict, tool: str, inp: dict) -> Any:
    base = settings.atlas_url

    if tool == "atlas_list_projects":
        params = {"limit": inp.get("limit", 20)}
        if inp.get("status") and inp["status"] != "all":
            params["status"] = inp["status"]
        r = await client.get(f"{base}/api/v1/projects/", headers=headers, params=params)
        return _parse(r)

    if tool == "atlas_create_project":
        r = await client.post(f"{base}/api/v1/projects/", headers=headers, json=inp)
        return _parse(r)

    if tool == "atlas_list_tasks":
        params = {"limit": inp.get("limit", 20)}
        if inp.get("project_id"):
            params["project_id"] = inp["project_id"]
        if inp.get("status") and inp["status"] != "all":
            params["status"] = inp["status"]
        if inp.get("assignee_id"):
            params["assignee_id"] = inp["assignee_id"]
        r = await client.get(f"{base}/api/v1/tasks/", headers=headers, params=params)
        return _parse(r)

    if tool == "atlas_create_task":
        r = await client.post(f"{base}/api/v1/tasks/", headers=headers, json=inp)
        return _parse(r)

    if tool == "atlas_update_task":
        task_id = inp.pop("task_id")
        r = await client.patch(f"{base}/api/v1/tasks/{task_id}", headers=headers, json=inp)
        return _parse(r)

    return {"error": f"Unhandled atlas tool: {tool}"}


# ─── CALENDAR ─────────────────────────────────────────────────────────────────

async def _calendar(client: httpx.AsyncClient, headers: dict, tool: str, inp: dict) -> Any:
    base = settings.calendar_url

    if tool == "calendar_list_events":
        params = {
            "start": inp["start_date"],
            "end": inp["end_date"],
            "limit": inp.get("limit", 20),
        }
        r = await client.get(f"{base}/api/events", headers=headers, params=params)
        return _parse(r)

    if tool == "calendar_create_event":
        payload = {
            "title": inp["title"],
            "start": inp["start"],
            "end": inp["end"],
            "description": inp.get("description", ""),
            "attendees": inp.get("attendees", []),
            "location": inp.get("location", ""),
        }
        r = await client.post(f"{base}/api/events", headers=headers, json=payload)
        return _parse(r)

    return {"error": f"Unhandled calendar tool: {tool}"}


# ─── CONNECT ──────────────────────────────────────────────────────────────────

async def _connect(client: httpx.AsyncClient, headers: dict, tool: str, inp: dict) -> Any:
    base = settings.connect_url

    if tool == "connect_list_channels":
        r = await client.get(f"{base}/api/initial-data", headers=headers)
        data = _parse(r)
        # Extract just channels for a clean response
        if isinstance(data, dict) and "channels" in data:
            return {"channels": data["channels"]}
        return data

    if tool == "connect_send_message":
        # Connect uses socket.io for real-time — for the agent we use the REST endpoint
        payload = {
            "channel_id": inp["channel_id"],
            "content": inp["message"],
        }
        r = await client.post(f"{base}/api/messages", headers=headers, json=payload)
        return _parse(r)

    if tool == "connect_search_messages":
        params = {"q": inp["query"], "limit": inp.get("limit", 10)}
        r = await client.get(f"{base}/api/search", headers=headers, params=params)
        return _parse(r)

    return {"error": f"Unhandled connect tool: {tool}"}


# ─── MAIL ─────────────────────────────────────────────────────────────────────

async def _mail(client: httpx.AsyncClient, headers: dict, tool: str, inp: dict) -> Any:
    base = settings.mail_url

    if tool == "mail_list_emails":
        params = {
            "folder": inp.get("folder", "inbox"),
            "limit": inp.get("limit", 10),
        }
        if inp.get("unread_only"):
            params["unread"] = True
        r = await client.get(f"{base}/api/v1/mail/", headers=headers, params=params)
        return _parse(r)

    if tool == "mail_send_email":
        payload = {
            "to": inp["to"],
            "subject": inp["subject"],
            "body": inp["body"],
            "cc": inp.get("cc", []),
        }
        r = await client.post(f"{base}/api/v1/mail/compose", headers=headers, json=payload)
        return _parse(r)

    if tool == "mail_search_emails":
        params = {"q": inp["query"], "limit": inp.get("limit", 10)}
        r = await client.get(f"{base}/api/v1/search", headers=headers, params=params)
        return _parse(r)

    return {"error": f"Unhandled mail tool: {tool}"}


# ─── WRITER ───────────────────────────────────────────────────────────────────

async def _writer(client: httpx.AsyncClient, headers: dict, tool: str, inp: dict) -> Any:
    base = settings.writer_url

    if tool == "writer_list_documents":
        params = {"limit": inp.get("limit", 20)}
        r = await client.get(f"{base}/api/v1/documents/", headers=headers, params=params)
        return _parse(r)

    if tool == "writer_create_document":
        payload = {"title": inp["title"]}
        r = await client.post(f"{base}/api/v1/documents/", headers=headers, json=payload)
        result = _parse(r)
        # If initial content was provided, add it as a block
        if isinstance(result, dict) and result.get("id") and inp.get("content"):
            doc_id = result["id"]
            block_payload = {
                "type": "paragraph",
                "content": inp["content"],
                "order": 0,
            }
            await client.post(
                f"{base}/api/v1/documents/{doc_id}/blocks",
                headers=headers,
                json=block_payload,
            )
        return result

    if tool == "writer_get_document":
        doc_id = inp["document_id"]
        r = await client.get(f"{base}/api/v1/documents/{doc_id}", headers=headers)
        blocks_r = await client.get(f"{base}/api/v1/documents/{doc_id}/blocks", headers=headers)
        doc = _parse(r)
        blocks = _parse(blocks_r)
        if isinstance(doc, dict):
            doc["blocks"] = blocks
        return doc

    return {"error": f"Unhandled writer tool: {tool}"}


# ─── PLANET ───────────────────────────────────────────────────────────────────

async def _planet(client: httpx.AsyncClient, headers: dict, tool: str, inp: dict) -> Any:
    base = settings.planet_url

    if tool == "planet_list_deals":
        params = {"limit": inp.get("limit", 20)}
        if inp.get("stage"):
            params["stage"] = inp["stage"]
        r = await client.get(f"{base}/api/v1/deals/", headers=headers, params=params)
        return _parse(r)

    if tool == "planet_create_deal":
        payload = {
            "name": inp["name"],
            "value": inp.get("value", 0),
            "stage": inp.get("stage", "prospect"),
            "contact_email": inp.get("contact_email", ""),
            "notes": inp.get("notes", ""),
        }
        r = await client.post(f"{base}/api/v1/deals/", headers=headers, json=payload)
        return _parse(r)

    if tool == "planet_list_contacts":
        # Derive contacts from deals — same logic as the Contacts page
        params = {"limit": 200}  # get all deals to derive contacts
        r = await client.get(f"{base}/api/v1/deals/", headers=headers, params=params)
        raw = _parse(r)
        deals = raw.get("deals", raw) if isinstance(raw, dict) else raw
        # Build contact map keyed by email or company+name
        contacts: dict = {}
        for d in (deals if isinstance(deals, list) else []):
            key = d.get("contact_email") or f"{d.get('company', '')}_{d.get('name', '')}"
            if key in contacts:
                contacts[key]["deal_count"] += 1
                contacts[key]["total_value"] += d.get("value", 0)
            else:
                contacts[key] = {
                    "name": d.get("name") or d.get("company", ""),
                    "company": d.get("company", ""),
                    "email": d.get("contact_email", ""),
                    "industry": d.get("industry", ""),
                    "region": d.get("region", ""),
                    "deal_count": 1,
                    "total_value": d.get("value", 0),
                    "latest_stage": d.get("stage", ""),
                }
        result = sorted(contacts.values(), key=lambda c: c["total_value"], reverse=True)
        # Apply search filter if provided
        if inp.get("search"):
            q = inp["search"].lower()
            result = [c for c in result if q in c["name"].lower() or q in c["company"].lower() or q in c["email"].lower()]
        limit = inp.get("limit", 20)
        return {"contacts": result[:limit], "total": len(result)}

    return {"error": f"Unhandled planet tool: {tool}"}


# ─── TURBOTICK ────────────────────────────────────────────────────────────────

async def _turbotick(client: httpx.AsyncClient, headers: dict, tool: str, inp: dict) -> Any:
    base = settings.turbotick_url

    if tool == "turbotick_list_tickets":
        params = {"limit": inp.get("limit", 20)}
        if inp.get("status") and inp["status"] != "all":
            params["status"] = inp["status"]
        if inp.get("priority"):
            params["priority"] = inp["priority"]
        r = await client.get(f"{base}/api/tickets", headers=headers, params=params)
        return _parse(r)

    if tool == "turbotick_create_ticket":
        payload = {
            "title": inp["title"],
            "description": inp.get("description", ""),
            "priority": inp.get("priority", "medium"),
            "type": inp.get("type", "support"),
        }
        r = await client.post(f"{base}/api/tickets", headers=headers, json=payload)
        return _parse(r)

    return {"error": f"Unhandled turbotick tool: {tool}"}


# ─── SEARCH ───────────────────────────────────────────────────────────────────

async def _search(client: httpx.AsyncClient, headers: dict, inp: dict) -> Any:
    base = settings.search_url
    params = {
        "q": inp["query"],
        "limit": inp.get("limit", 5),
    }
    if inp.get("sources"):
        params["sources"] = ",".join(inp["sources"])
    r = await client.get(f"{base}/api/search", headers=headers, params=params)
    return _parse(r)


# ─── CAPITAL HUB ──────────────────────────────────────────────────────────────

async def _capital(client: httpx.AsyncClient, headers: dict, tool: str, inp: dict) -> Any:
    base = settings.capital_hub_url

    if tool == "capital_list_transactions":
        params = {"limit": inp.get("limit", 20)}
        r = await client.get(f"{base}/api/v1/finance/transactions", headers=headers, params=params)
        return _parse(r)

    if tool == "capital_log_expense":
        payload = {
            "description": inp["description"],
            "amount": inp["amount"],
            "category": inp.get("category", "general"),
            "type": "expense",
        }
        r = await client.post(f"{base}/api/v1/finance/transactions", headers=headers, json=payload)
        return _parse(r)

    return {"error": f"Unhandled capital tool: {tool}"}


# ─── MEET ─────────────────────────────────────────────────────────────────────

async def _meet(client: httpx.AsyncClient, headers: dict, inp: dict) -> Any:
    # Meet is UI-driven; we generate a room link and return it for the user to click
    import uuid
    room_id = str(uuid.uuid4())[:8]
    meet_base = "https://meet.freedomlabs.in"
    return {
        "room_id": room_id,
        "title": inp["title"],
        "join_url": f"{meet_base}/room/{room_id}",
        "message": f"Meeting room created. Share this link to join: {meet_base}/room/{room_id}",
    }


async def _meet_pre_call_brief(client: httpx.AsyncClient, headers: dict, inp: dict) -> Any:
    meeting_id = inp["meeting_id"]
    params = {}
    if inp.get("title"):
        params["title"] = inp["title"]
    if inp.get("participants"):
        params["participants"] = ",".join(inp["participants"])
    r = await client.get(
        f"{settings.meet_url}/api/meetings/{meeting_id}/brief",
        headers=headers,
        params=params,
        timeout=30.0,
    )
    return _parse(r)


async def _meet_post_call_sync(client: httpx.AsyncClient, headers: dict, inp: dict) -> Any:
    meeting_id = inp["meeting_id"]
    body = {
        "title": inp.get("title", meeting_id),
        "attendee_emails": inp.get("attendee_emails", []),
        "atlas_project_id": inp.get("atlas_project_id"),
    }
    r = await client.post(
        f"{settings.meet_url}/api/meetings/{meeting_id}/post-call-sync",
        headers=headers,
        json=body,
        timeout=60.0,
    )
    return _parse(r)


# ─── RM WALLET ────────────────────────────────────────────────────────────────

async def _wallet(client: httpx.AsyncClient, headers: dict, tool: str, inp: dict) -> Any:
    base = settings.wallet_url

    if tool == "wallet_list_secrets":
        params = {"limit": inp.get("limit", 20)}
        if inp.get("search"):
            params["search"] = inp["search"]
        r = await client.get(f"{base}/api/wallet/secrets", headers=headers, params=params)
        result = _parse(r)
        # Strip any 'value' fields from response for security
        if isinstance(result, dict) and "secrets" in result:
            for s in result["secrets"]:
                s.pop("value", None)
        return result

    if tool == "wallet_create_secret":
        payload = {
            "name": inp["name"],
            "value": inp["value"],
            "tags": inp.get("tags", []),
        }
        if inp.get("expires_at"):
            payload["expires_at"] = inp["expires_at"]
        r = await client.post(f"{base}/api/wallet/secrets", headers=headers, json=payload)
        result = _parse(r)
        # Never return the stored value in the response
        if isinstance(result, dict):
            result.pop("value", None)
        return result

    return {"error": f"Unhandled wallet tool: {tool}"}


# ─── RM DOCK ──────────────────────────────────────────────────────────────────

async def _dock(client: httpx.AsyncClient, headers: dict, tool: str, inp: dict) -> Any:
    base = settings.dock_url

    if tool == "dock_list_apps":
        params = {"limit": inp.get("limit", 20)}
        if inp.get("category"):
            params["category"] = inp["category"]
        r = await client.get(f"{base}/api/dock/apps", headers=headers, params=params)
        return _parse(r)

    if tool == "dock_list_licenses":
        params = {"limit": inp.get("limit", 20)}
        r = await client.get(f"{base}/api/dock/licenses", headers=headers, params=params)
        return _parse(r)

    if tool == "dock_request_access":
        payload = {
            "app_id": inp["app_id"],
            "justification": inp["justification"],
        }
        r = await client.post(f"{base}/api/dock/requests", headers=headers, json=payload)
        return _parse(r)

    return {"error": f"Unhandled dock tool: {tool}"}


# ─── FITTERME ─────────────────────────────────────────────────────────────────

async def _fitterme(client: httpx.AsyncClient, headers: dict, tool: str, inp: dict) -> Any:
    base = settings.fitterme_url
    user_id = "user-demo"  # resolved from auth token in production

    if tool == "fitterme_get_dashboard":
        r = await client.get(f"{base}/v1/dashboard/{user_id}", headers=headers)
        return _parse(r)

    if tool == "fitterme_log_workout":
        payload = {
            "user_id": user_id,
            "session_name": inp["session_name"],
            "duration_minutes": inp["duration_minutes"],
            "exercises_completed": 0,
            "notes": inp.get("notes", ""),
        }
        r = await client.post(f"{base}/v1/workouts/logs", headers=headers, json=payload)
        return _parse(r)

    if tool == "fitterme_get_coach":
        r = await client.get(f"{base}/v1/coach/recommendation/{user_id}", headers=headers)
        return _parse(r)

    return {"error": f"Unhandled fitterme tool: {tool}"}


# ─── SECURE ───────────────────────────────────────────────────────────────────

async def _secure(client: httpx.AsyncClient, headers: dict, tool: str, inp: dict) -> Any:
    base = settings.secure_url

    if tool == "secure_get_overview":
        r = await client.get(f"{base}/api/v1/overview", headers=headers)
        return _parse(r)

    if tool == "secure_list_vulnerabilities":
        params = {"limit": inp.get("limit", 20)}
        if inp.get("severity") and inp["severity"] != "all":
            params["severity"] = inp["severity"]
        r = await client.get(f"{base}/api/v1/vulnerabilities", headers=headers, params=params)
        return _parse(r)

    return {"error": f"Unhandled secure tool: {tool}"}


# ─── POWER TOOLS (composite multi-service) ───────────────────────────────────
# Each fans out to multiple services concurrently via asyncio.gather.
# The AI synthesizes the combined result into a structured response.
# Inspired by gstack's /daily-brief, /sprint, /retro, /plan-ceo-review, /cso.


async def _orbit_daily_brief(client: httpx.AsyncClient, headers: dict, inp: dict) -> Any:
    today = inp.get("date") or str(date.today())
    tomorrow = str(date.fromisoformat(today) + timedelta(days=1))
    user_id = "user-demo"

    calendar_r, mail_r, tasks_r, tickets_r, health_r = await asyncio.gather(
        client.get(f"{settings.calendar_url}/api/events", headers=headers,
                   params={"start": today, "end": tomorrow, "limit": 20}),
        client.get(f"{settings.mail_url}/api/v1/mail/", headers=headers,
                   params={"folder": "inbox", "limit": 5, "unread": True}),
        client.get(f"{settings.atlas_url}/api/v1/tasks/", headers=headers,
                   params={"status": "in_progress", "limit": 20}),
        client.get(f"{settings.turbotick_url}/api/tickets", headers=headers,
                   params={"status": "open", "priority": "critical", "limit": 10}),
        client.get(f"{settings.fitterme_url}/v1/dashboard/{user_id}", headers=headers),
    )

    return {
        "date": today,
        "calendar_today": _parse(calendar_r),
        "unread_mail": _parse(mail_r),
        "tasks_in_progress": _parse(tasks_r),
        "critical_tickets": _parse(tickets_r),
        "health_dashboard": _parse(health_r),
    }


async def _orbit_sprint_plan(client: httpx.AsyncClient, headers: dict, inp: dict) -> Any:
    params_backlog = {"status": "todo", "limit": 30}
    params_prog = {"status": "in_progress", "limit": 20}
    if inp.get("project_id"):
        params_backlog["project_id"] = inp["project_id"]
        params_prog["project_id"] = inp["project_id"]

    backlog_r, inprog_r = await asyncio.gather(
        client.get(f"{settings.atlas_url}/api/v1/tasks/", headers=headers, params=params_backlog),
        client.get(f"{settings.atlas_url}/api/v1/tasks/", headers=headers, params=params_prog),
    )

    return {
        "sprint_name": inp.get("sprint_name", "Next Sprint"),
        "duration_days": inp.get("duration_days", 14),
        "start_date": inp.get("start_date"),
        "backlog": _parse(backlog_r),
        "in_progress": _parse(inprog_r),
        "instruction": (
            "Analyze backlog and in_progress. Propose sprint scope (which tasks to commit), "
            "suggested assignees, realistic timeline, and top 2-3 risks. "
            "Format as: Goal | In Flight | Planned | Risks."
        ),
    }


async def _orbit_retrospective(client: httpx.AsyncClient, headers: dict, inp: dict) -> Any:
    period = inp.get("period_days", 14)
    from_date = str(date.today() - timedelta(days=period))

    params_done = {"status": "done", "limit": 50}
    params_tickets = {"status": "resolved", "limit": 30}
    if inp.get("project_id"):
        params_done["project_id"] = inp["project_id"]

    done_r, tickets_r = await asyncio.gather(
        client.get(f"{settings.atlas_url}/api/v1/tasks/", headers=headers, params=params_done),
        client.get(f"{settings.turbotick_url}/api/tickets", headers=headers, params=params_tickets),
    )

    return {
        "period_days": period,
        "from_date": from_date,
        "to_date": str(date.today()),
        "completed_tasks": _parse(done_r),
        "resolved_tickets": _parse(tickets_r),
        "instruction": (
            "Analyze completed work vs what a healthy sprint should look like. "
            "Identify: ✅ Wins | ⚠️ Blockers | 🔄 Patterns | 📋 Action Items. "
            "End with 2-3 concrete action items to create as Atlas tasks."
        ),
    }


async def _orbit_pipeline_review(client: httpx.AsyncClient, headers: dict, inp: dict) -> Any:
    deals_r = await client.get(
        f"{settings.planet_url}/api/v1/deals/", headers=headers, params={"limit": 100}
    )
    deals_raw = _parse(deals_r)
    deals = deals_raw.get("deals", deals_raw) if isinstance(deals_raw, dict) else deals_raw

    # Summarize pipeline by stage
    stage_summary: dict = {}
    stale_deals = []
    total_value = 0.0

    for d in (deals if isinstance(deals, list) else []):
        stage = d.get("stage", "unknown")
        val = d.get("value", 0) or 0
        total_value += val
        if stage not in stage_summary:
            stage_summary[stage] = {"count": 0, "value": 0.0}
        stage_summary[stage]["count"] += 1
        stage_summary[stage]["value"] += val
        # Flag deals with no recent notes as potentially stale
        if not d.get("notes") and stage not in ("closed_won", "closed_lost"):
            stale_deals.append({"name": d.get("name"), "stage": stage, "value": val})

    result: dict = {
        "total_deals": len(deals) if isinstance(deals, list) else 0,
        "total_pipeline_value": total_value,
        "pipeline_by_stage": stage_summary,
        "stale_deals": stale_deals[:10],
        "raw_deals": deals[:50] if isinstance(deals, list) else deals,
    }

    if inp.get("include_contacts", True):
        contacts_r = await client.get(
            f"{settings.planet_url}/api/v1/deals/", headers=headers, params={"limit": 200}
        )
        all_deals = _parse(contacts_r)
        all_list = all_deals.get("deals", all_deals) if isinstance(all_deals, dict) else all_deals
        contacts: dict = {}
        for d in (all_list if isinstance(all_list, list) else []):
            key = d.get("contact_email") or f"{d.get('company', '')}_{d.get('name', '')}"
            if key not in contacts:
                contacts[key] = {"name": d.get("name", ""), "email": d.get("contact_email", ""),
                                 "deal_count": 0, "total_value": 0.0, "latest_stage": ""}
            contacts[key]["deal_count"] += 1
            contacts[key]["total_value"] += d.get("value", 0) or 0
            contacts[key]["latest_stage"] = d.get("stage", "")
        top_contacts = sorted(contacts.values(), key=lambda c: c["total_value"], reverse=True)[:10]
        result["top_contacts"] = top_contacts

    result["instruction"] = (
        "Analyze pipeline health: stage distribution, velocity signals, stale deals needing follow-up. "
        "Recommend 3-5 prioritized outreach actions with deal names and suggested next steps."
    )
    return result


async def _orbit_security_audit(client: httpx.AsyncClient, headers: dict, _inp: dict) -> Any:
    overview_r, vulns_r, secrets_r, apps_r, incidents_r = await asyncio.gather(
        client.get(f"{settings.secure_url}/api/v1/overview", headers=headers),
        client.get(f"{settings.secure_url}/api/v1/vulnerabilities", headers=headers,
                   params={"severity": "critical", "limit": 20}),
        client.get(f"{settings.wallet_url}/api/wallet/secrets", headers=headers,
                   params={"limit": 50}),
        client.get(f"{settings.dock_url}/api/dock/apps", headers=headers, params={"limit": 50}),
        client.get(f"{settings.turbotick_url}/api/tickets", headers=headers,
                   params={"status": "open", "type": "incident", "limit": 10}),
    )

    secrets = _parse(secrets_r)
    # Never expose secret values — strip them defensively
    if isinstance(secrets, dict) and "secrets" in secrets:
        for s in secrets["secrets"]:
            s.pop("value", None)

    return {
        "security_overview": _parse(overview_r),
        "critical_vulnerabilities": _parse(vulns_r),
        "secret_inventory": secrets,
        "software_catalog": _parse(apps_r),
        "open_incidents": _parse(incidents_r),
        "audit_framework": "OWASP Top 10 + STRIDE",
        "instruction": (
            "Apply OWASP Top 10 and STRIDE threat model. Triage findings: "
            "Critical (fix now) > High (this sprint) > Medium (backlog). "
            "Flag secrets with no expiry. Flag unauthorized or unlicensed software. "
            "End with a risk score (1-10) and top 3 remediation actions."
        ),
    }


# ─── HELPERS ──────────────────────────────────────────────────────────────────

def _parse(response: httpx.Response) -> Any:
    try:
        data = response.json()
    except Exception:
        data = {"raw": response.text}

    if response.status_code >= 400:
        return {
            "error": f"Service returned {response.status_code}",
            "detail": data,
        }
    return data
