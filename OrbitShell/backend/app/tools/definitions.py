"""
Tool definitions for all RM Orbit services.
These are passed to Claude as its action toolkit.
"""

ORBIT_TOOLS = [
    # ─── ATLAS ───────────────────────────────────────────────────────────────
    {
        "name": "atlas_list_projects",
        "description": "List all projects in the workspace. Use this to show the user their current projects or to find a project before creating tasks.",
        "input_schema": {
            "type": "object",
            "properties": {
                "status": {
                    "type": "string",
                    "enum": ["active", "archived", "all"],
                    "description": "Filter by project status. Defaults to active."
                },
                "limit": {"type": "integer", "description": "Max results, default 20"}
            },
            "required": []
        }
    },
    {
        "name": "atlas_create_project",
        "description": "Create a new project in Atlas project management.",
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Project name"},
                "description": {"type": "string", "description": "Project description"},
                "color": {"type": "string", "description": "Hex color code e.g. #4F46E5"}
            },
            "required": ["name"]
        }
    },
    {
        "name": "atlas_list_tasks",
        "description": "List tasks, optionally filtered by project, assignee, or status.",
        "input_schema": {
            "type": "object",
            "properties": {
                "project_id": {"type": "string", "description": "Filter by project ID"},
                "status": {
                    "type": "string",
                    "enum": ["todo", "in_progress", "done", "all"],
                    "description": "Filter by task status"
                },
                "assignee_id": {"type": "string", "description": "Filter by assignee user ID"},
                "limit": {"type": "integer", "description": "Max results, default 20"}
            },
            "required": []
        }
    },
    {
        "name": "atlas_create_task",
        "description": "Create a new task in a project.",
        "input_schema": {
            "type": "object",
            "properties": {
                "project_id": {"type": "string", "description": "The project to add the task to"},
                "title": {"type": "string", "description": "Task title"},
                "description": {"type": "string", "description": "Task description or details"},
                "assignee_id": {"type": "string", "description": "User ID to assign the task to"},
                "due_date": {"type": "string", "description": "Due date in ISO format e.g. 2026-04-15"},
                "priority": {
                    "type": "string",
                    "enum": ["low", "medium", "high", "urgent"],
                    "description": "Task priority"
                }
            },
            "required": ["project_id", "title"]
        }
    },
    {
        "name": "atlas_update_task",
        "description": "Update an existing task — change status, assignee, due date, or title.",
        "input_schema": {
            "type": "object",
            "properties": {
                "task_id": {"type": "string", "description": "The task ID to update"},
                "title": {"type": "string"},
                "status": {"type": "string", "enum": ["todo", "in_progress", "done"]},
                "assignee_id": {"type": "string"},
                "due_date": {"type": "string"},
                "priority": {"type": "string", "enum": ["low", "medium", "high", "urgent"]}
            },
            "required": ["task_id"]
        }
    },

    # ─── CALENDAR ────────────────────────────────────────────────────────────
    {
        "name": "calendar_list_events",
        "description": "List calendar events within a date range.",
        "input_schema": {
            "type": "object",
            "properties": {
                "start_date": {"type": "string", "description": "Start date ISO format e.g. 2026-03-27"},
                "end_date": {"type": "string", "description": "End date ISO format e.g. 2026-04-03"},
                "limit": {"type": "integer", "description": "Max events to return, default 20"}
            },
            "required": ["start_date", "end_date"]
        }
    },
    {
        "name": "calendar_create_event",
        "description": "Create a calendar event or meeting.",
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Event title"},
                "start": {"type": "string", "description": "Start datetime ISO format e.g. 2026-03-28T10:00:00"},
                "end": {"type": "string", "description": "End datetime ISO format e.g. 2026-03-28T11:00:00"},
                "description": {"type": "string", "description": "Event description or agenda"},
                "attendees": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of attendee email addresses or user IDs"
                },
                "location": {"type": "string", "description": "Physical or virtual meeting location/link"}
            },
            "required": ["title", "start", "end"]
        }
    },

    # ─── CONNECT (CHAT) ───────────────────────────────────────────────────────
    {
        "name": "connect_list_channels",
        "description": "List available chat channels in the workspace.",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "connect_send_message",
        "description": "Send a message to a chat channel.",
        "input_schema": {
            "type": "object",
            "properties": {
                "channel_id": {"type": "string", "description": "The channel ID to send to"},
                "message": {"type": "string", "description": "The message content"}
            },
            "required": ["channel_id", "message"]
        }
    },
    {
        "name": "connect_search_messages",
        "description": "Search through past chat messages.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"},
                "limit": {"type": "integer", "description": "Max results, default 10"}
            },
            "required": ["query"]
        }
    },

    # ─── MAIL ────────────────────────────────────────────────────────────────
    {
        "name": "mail_list_emails",
        "description": "List emails from inbox or a specific folder.",
        "input_schema": {
            "type": "object",
            "properties": {
                "folder": {
                    "type": "string",
                    "enum": ["inbox", "sent", "drafts", "starred"],
                    "description": "Which folder to list. Defaults to inbox."
                },
                "unread_only": {"type": "boolean", "description": "Only show unread emails"},
                "limit": {"type": "integer", "description": "Max results, default 10"}
            },
            "required": []
        }
    },
    {
        "name": "mail_send_email",
        "description": "Send an email.",
        "input_schema": {
            "type": "object",
            "properties": {
                "to": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Recipient email addresses"
                },
                "subject": {"type": "string"},
                "body": {"type": "string", "description": "Email body, supports basic HTML"},
                "cc": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "CC email addresses"
                }
            },
            "required": ["to", "subject", "body"]
        }
    },
    {
        "name": "mail_search_emails",
        "description": "Search through emails.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search terms"},
                "limit": {"type": "integer", "description": "Max results, default 10"}
            },
            "required": ["query"]
        }
    },

    # ─── WRITER (DOCS) ────────────────────────────────────────────────────────
    {
        "name": "writer_list_documents",
        "description": "List documents in the workspace.",
        "input_schema": {
            "type": "object",
            "properties": {
                "limit": {"type": "integer", "description": "Max results, default 20"}
            },
            "required": []
        }
    },
    {
        "name": "writer_create_document",
        "description": "Create a new document in Writer.",
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Document title"},
                "content": {"type": "string", "description": "Initial document content (markdown or plain text)"}
            },
            "required": ["title"]
        }
    },
    {
        "name": "writer_get_document",
        "description": "Read the content of a document.",
        "input_schema": {
            "type": "object",
            "properties": {
                "document_id": {"type": "string", "description": "Document ID"}
            },
            "required": ["document_id"]
        }
    },

    # ─── PLANET (CRM) ─────────────────────────────────────────────────────────
    {
        "name": "planet_list_deals",
        "description": "List deals in the CRM pipeline.",
        "input_schema": {
            "type": "object",
            "properties": {
                "stage": {
                    "type": "string",
                    "description": "Filter by pipeline stage e.g. prospect, qualified, proposal, closed_won"
                },
                "limit": {"type": "integer", "description": "Max results, default 20"}
            },
            "required": []
        }
    },
    {
        "name": "planet_create_deal",
        "description": "Create a new deal/lead in the CRM.",
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Deal name or contact name"},
                "value": {"type": "number", "description": "Deal value in USD"},
                "stage": {"type": "string", "description": "Pipeline stage, default is prospect"},
                "contact_email": {"type": "string", "description": "Contact email address"},
                "notes": {"type": "string", "description": "Initial notes about the deal"}
            },
            "required": ["name"]
        }
    },
    {
        "name": "planet_list_contacts",
        "description": "List unique contacts derived from CRM deal records, including their associated deals and pipeline value.",
        "input_schema": {
            "type": "object",
            "properties": {
                "search": {"type": "string", "description": "Search by name, company, or email"},
                "limit": {"type": "integer", "description": "Max results, default 20"}
            },
            "required": []
        }
    },

    # ─── TURBOTICK (SUPPORT/TICKETS) ──────────────────────────────────────────
    {
        "name": "turbotick_list_tickets",
        "description": "List support tickets or incidents.",
        "input_schema": {
            "type": "object",
            "properties": {
                "status": {
                    "type": "string",
                    "enum": ["open", "in_progress", "resolved", "closed", "all"],
                    "description": "Filter by ticket status"
                },
                "priority": {
                    "type": "string",
                    "enum": ["low", "medium", "high", "critical"],
                    "description": "Filter by priority"
                },
                "limit": {"type": "integer", "description": "Max results, default 20"}
            },
            "required": []
        }
    },
    {
        "name": "turbotick_create_ticket",
        "description": "Create a support ticket or incident report.",
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Ticket title"},
                "description": {"type": "string", "description": "Detailed description of the issue"},
                "priority": {
                    "type": "string",
                    "enum": ["low", "medium", "high", "critical"],
                    "description": "Ticket priority, default is medium"
                },
                "type": {
                    "type": "string",
                    "enum": ["bug", "feature", "support", "incident"],
                    "description": "Ticket type"
                }
            },
            "required": ["title"]
        }
    },

    # ─── SEARCH (CROSS-SERVICE) ───────────────────────────────────────────────
    {
        "name": "orbit_search",
        "description": "Search across all Orbit services at once — projects, tasks, documents, emails, deals, and more.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"},
                "sources": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": ["atlas", "mail", "writer", "planet", "turbotick", "learn"]
                    },
                    "description": "Limit search to specific services. Empty means search all."
                },
                "limit": {"type": "integer", "description": "Max results per source, default 5"}
            },
            "required": ["query"]
        }
    },

    # ─── CAPITAL HUB (FINANCE) ────────────────────────────────────────────────
    {
        "name": "capital_list_transactions",
        "description": "List financial transactions or expenses.",
        "input_schema": {
            "type": "object",
            "properties": {
                "limit": {"type": "integer", "description": "Max results, default 20"}
            },
            "required": []
        }
    },
    {
        "name": "capital_log_expense",
        "description": "Log a new expense or financial transaction.",
        "input_schema": {
            "type": "object",
            "properties": {
                "description": {"type": "string", "description": "What the expense was for"},
                "amount": {"type": "number", "description": "Amount in USD"},
                "category": {"type": "string", "description": "Category e.g. software, travel, marketing"}
            },
            "required": ["description", "amount"]
        }
    },

    # ─── MEET (deep link only — no direct control) ────────────────────────────
    {
        "name": "meet_create_room",
        "description": "Create a Meet video room and return the join link. The user will need to click the link to join.",
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Meeting room title"},
                "scheduled_at": {"type": "string", "description": "Optional ISO datetime for scheduled meetings"}
            },
            "required": ["title"]
        }
    },

    # ─── RM WALLET (SECRETS VAULT) ───────────────────────────────────────────
    {
        "name": "wallet_list_secrets",
        "description": "List secret entries in the RM Wallet vault (names and metadata only — values are never returned). Use this to help the user find a stored credential or API key.",
        "input_schema": {
            "type": "object",
            "properties": {
                "search": {"type": "string", "description": "Optional search term to filter by secret name or tag"},
                "limit": {"type": "integer", "description": "Max results, default 20"}
            },
            "required": []
        }
    },
    {
        "name": "wallet_create_secret",
        "description": "Store a new secret in the RM Wallet vault. The value is encrypted at rest.",
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Secret name or label e.g. 'Stripe API Key'"},
                "value": {"type": "string", "description": "The secret value to encrypt and store"},
                "tags": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional tags for categorization e.g. ['api-keys', 'production']"
                },
                "expires_at": {"type": "string", "description": "Optional ISO expiry datetime"}
            },
            "required": ["name", "value"]
        }
    },

    # ─── RM DOCK (SOFTWARE & LICENSE PORTAL) ─────────────────────────────────
    {
        "name": "dock_list_apps",
        "description": "List software apps/tools available in the RM Dock catalog for the organization.",
        "input_schema": {
            "type": "object",
            "properties": {
                "category": {"type": "string", "description": "Filter by category e.g. 'productivity', 'security', 'devtools'"},
                "limit": {"type": "integer", "description": "Max results, default 20"}
            },
            "required": []
        }
    },
    {
        "name": "dock_list_licenses",
        "description": "List software licenses owned by the organization, including seat usage.",
        "input_schema": {
            "type": "object",
            "properties": {
                "limit": {"type": "integer", "description": "Max results, default 20"}
            },
            "required": []
        }
    },
    {
        "name": "dock_request_access",
        "description": "Submit a software access request for an app in the Dock catalog.",
        "input_schema": {
            "type": "object",
            "properties": {
                "app_id": {"type": "string", "description": "The app ID to request access to"},
                "justification": {"type": "string", "description": "Business justification for the access request"}
            },
            "required": ["app_id", "justification"]
        }
    },

    # ─── FITTERME (ECOSYSTEM HEALTH) ─────────────────────────────────────────
    {
        "name": "fitterme_get_dashboard",
        "description": "Get the user's current health dashboard — readiness score, streak, workouts this week, calories today, and habit completion.",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "fitterme_log_workout",
        "description": "Log a completed workout session for the user.",
        "input_schema": {
            "type": "object",
            "properties": {
                "session_name": {"type": "string", "description": "Name of the workout session e.g. 'Upper Body Strength'"},
                "duration_minutes": {"type": "integer", "description": "How long the workout lasted in minutes"},
                "notes": {"type": "string", "description": "Optional notes about how it went"}
            },
            "required": ["session_name", "duration_minutes"]
        }
    },
    {
        "name": "fitterme_get_coach",
        "description": "Get the AI coach's daily recommendation for the user based on recovery metrics, training history, and goals.",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },

    # ─── SECURE (COMPLIANCE) ─────────────────────────────────────────────────
    {
        "name": "secure_get_overview",
        "description": "Get the security and compliance overview — overall risk score, policy counts, open vulnerabilities, and endpoint status.",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "secure_list_vulnerabilities",
        "description": "List open security vulnerabilities tracked in the Secure compliance module.",
        "input_schema": {
            "type": "object",
            "properties": {
                "severity": {
                    "type": "string",
                    "enum": ["critical", "high", "medium", "low", "all"],
                    "description": "Filter by severity level"
                },
                "limit": {"type": "integer", "description": "Max results, default 20"}
            },
            "required": []
        }
    },

    # ─── POWER TOOLS (composite multi-service queries) ────────────────────────
    # Inspired by gstack's sprint, retro, /cso, and daily-brief workflows.
    # Each fans out to multiple Orbit services in parallel and returns a
    # combined result for the AI to synthesize into a structured response.

    {
        "name": "orbit_daily_brief",
        "description": (
            "Get a complete daily briefing aggregated across all services: today's calendar events, "
            "unread emails, tasks in progress, open critical tickets, and health readiness score. "
            "Call this when the user asks for a morning briefing, daily standup, or status overview. "
            "Pulls from Calendar, Mail, Atlas, TurboTick, and FitterMe in parallel."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "Date for the brief ISO format e.g. 2026-04-24. Defaults to today."
                }
            },
            "required": []
        }
    },
    {
        "name": "orbit_sprint_plan",
        "description": (
            "Run a sprint planning session: pulls current backlog (todo tasks) and in-progress work from Atlas, "
            "then the AI proposes prioritized sprint scope, task assignments, timeline, and risks. "
            "Optionally creates a sprint kick-off calendar event. "
            "Call this when the user wants to plan a sprint, start a new cycle, or review backlog priority."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "sprint_name": {"type": "string", "description": "Sprint name e.g. 'Sprint 12'"},
                "duration_days": {"type": "integer", "description": "Sprint length in days, default 14"},
                "start_date": {"type": "string", "description": "Sprint start date ISO format e.g. 2026-04-28"},
                "project_id": {"type": "string", "description": "Atlas project ID to pull backlog from. Omit for all projects."}
            },
            "required": []
        }
    },
    {
        "name": "orbit_retrospective",
        "description": (
            "Run a sprint retrospective: pulls completed tasks and resolved tickets for the given period, "
            "then the AI identifies wins, blockers, patterns, and generates concrete action items. "
            "Call this when the user wants a retro, end-of-sprint review, or wants to understand what blocked the team."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "period_days": {
                    "type": "integer",
                    "description": "How many days back to analyze, default 14 (one sprint)"
                },
                "project_id": {
                    "type": "string",
                    "description": "Limit analysis to a specific Atlas project. Omit for all projects."
                }
            },
            "required": []
        }
    },
    {
        "name": "orbit_pipeline_review",
        "description": (
            "Full CRM pipeline health review: pulls all deals and contacts, "
            "then the AI analyzes pipeline value by stage, identifies stale deals, "
            "flags deals needing follow-up, and recommends prioritized outreach actions. "
            "Call this for any pipeline health, revenue forecast, or sales strategy question."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "include_contacts": {
                    "type": "boolean",
                    "description": "Include top contacts ranked by pipeline value, default true"
                }
            },
            "required": []
        }
    },
    {
        "name": "orbit_security_audit",
        "description": (
            "Comprehensive security posture audit using OWASP Top 10 and STRIDE threat model. "
            "Pulls data from Secure (vulnerabilities, compliance), Wallet (secret hygiene), "
            "Dock (software catalog risks), and TurboTick (open incidents) in parallel. "
            "Call this when the user asks for a security review, compliance check, or vulnerability triage."
        ),
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },

    # ─── MEET: PRE-CALL BRIEF ─────────────────────────────────────────────────
    {
        "name": "meet_get_pre_call_brief",
        "description": "Get an AI-generated briefing card before joining a meeting. Returns context from previous meetings with the same participants, open action items, and suggested talking points. Call this when the user is about to join a meeting or asks for meeting context.",
        "input_schema": {
            "type": "object",
            "properties": {
                "meeting_id": {"type": "string", "description": "The meeting ID"},
                "title": {"type": "string", "description": "Meeting title or topic"},
                "participants": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of participant names attending the meeting"
                }
            },
            "required": ["meeting_id"]
        }
    },

    # ─── MEET: POST-CALL SYNC ─────────────────────────────────────────────────
    {
        "name": "meet_post_call_sync",
        "description": "After a meeting ends, automatically create Atlas tasks from action items and draft a follow-up email. Call this when the user asks to wrap up a meeting, sync meeting outcomes, or create follow-up tasks from a call.",
        "input_schema": {
            "type": "object",
            "properties": {
                "meeting_id": {"type": "string", "description": "The meeting ID that just ended"},
                "title": {"type": "string", "description": "Meeting title"},
                "attendee_emails": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Email addresses of attendees for the follow-up draft"
                },
                "atlas_project_id": {"type": "string", "description": "Atlas project to add action item tasks to (optional)"}
            },
            "required": ["meeting_id"]
        }
    },
]

# Ollama uses OpenAI-compatible tool format: `parameters` instead of `input_schema`
OLLAMA_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": t["name"],
            "description": t["description"],
            "parameters": t["input_schema"],
        },
    }
    for t in ORBIT_TOOLS
]
