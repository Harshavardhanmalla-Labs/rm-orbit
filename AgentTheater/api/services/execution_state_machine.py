"""Strict state machine enforcement for Execution lifecycle."""


class ExecutionStateMachine:
    """Enforce valid execution state transitions."""

    # Valid transitions: from_state -> [valid_to_states]
    VALID_TRANSITIONS = {
        "approved": ["assigned", "in_progress", "blocked", "abandoned"],
        "assigned": ["in_progress", "blocked", "approved", "abandoned"],
        "in_progress": ["blocked", "completed", "approved", "abandoned"],
        "blocked": ["in_progress", "approved", "abandoned"],
        "completed": ["succeeded", "failed", "pivoted"],
        "succeeded": [],   # Terminal state
        "failed": [],      # Terminal state
        "pivoted": [],     # Terminal state
        "abandoned": [],   # Terminal state
    }

    @classmethod
    def is_valid_transition(cls, from_state: str, to_state: str) -> bool:
        """Check if transition is valid."""
        if from_state not in cls.VALID_TRANSITIONS:
            return False
        return to_state in cls.VALID_TRANSITIONS[from_state]

    @classmethod
    def validate_transition(cls, from_state: str, to_state: str) -> None:
        """Validate transition, raise ValueError if invalid."""
        if not cls.is_valid_transition(from_state, to_state):
            valid = cls.VALID_TRANSITIONS.get(from_state, [])
            raise ValueError(
                f"Invalid transition from '{from_state}' to '{to_state}'. "
                f"Valid transitions: {valid}"
            )

    @classmethod
    def get_valid_transitions(cls, state: str) -> list:
        """Get list of valid next states."""
        return cls.VALID_TRANSITIONS.get(state, [])

    @classmethod
    def is_terminal_state(cls, state: str) -> bool:
        """Check if state is terminal (no further transitions)."""
        return cls.VALID_TRANSITIONS.get(state, []) == []
