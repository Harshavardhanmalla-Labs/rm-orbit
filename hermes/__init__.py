"""
Hermes integration for RM Orbit.

Shared module that gives every Orbit service:
  - HermesAI     : LLM inference (Ollama local → OpenRouter cloud)
  - HermesMemory : Persistent FTS5 memory across services
  - HermesNotify : Multi-platform notifications (Telegram, Discord, Slack, etc.)

Usage from any Orbit service:
    from hermes import HermesAI, HermesMemory, HermesNotify
"""

from .ai import HermesAI
from .memory import HermesMemory
from .notify import HermesNotify

__all__ = ["HermesAI", "HermesMemory", "HermesNotify"]
