"""
memory.py
---------
Simple in-session conversation memory for the AI IT Helpdesk Agent.

This is intentionally lightweight (a Python list of dicts) since the
project only needs to remember the conversation for the current
Streamlit session, not across sessions or users.
"""

from datetime import datetime


class ConversationMemory:
    """Stores the running history of a single chat session."""

    def __init__(self):
        self._history = []  # list of {"role": "user"/"agent", "message": str,
                             #           "category": str or None, "timestamp": str}

    def add_message(self, role: str, message: str, category: str = None):
        """Add a message to the conversation history."""
        if role not in ("user", "agent"):
            raise ValueError("role must be 'user' or 'agent'")
        self._history.append({
            "role": role,
            "message": message,
            "category": category,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        })

    def get_history(self):
        """Return the full conversation history."""
        return list(self._history)

    def get_recent_messages(self, n: int = 5):
        """Return the last n messages (default 5)."""
        if n <= 0:
            return []
        return self._history[-n:]

    def get_last_user_category(self):
        """
        Convenience helper for the agent: find the category of the most
        recent user message that had one detected, so follow-up messages
        like "I already restarted the router" can be understood in context.
        """
        for entry in reversed(self._history):
            if entry["role"] == "user" and entry.get("category"):
                return entry["category"]
        return None

    def clear(self):
        """Clear the entire conversation history."""
        self._history = []

    def __len__(self):
        return len(self._history)


if __name__ == "__main__":
    mem = ConversationMemory()
    mem.add_message("user", "My Wi-Fi isn't working.", category="network")
    mem.add_message("agent", "Try restarting your router.")
    mem.add_message("user", "I already restarted the router.", category="network")
    print("History:", mem.get_history())
    print("Recent 1:", mem.get_recent_messages(1))
    print("Last user category:", mem.get_last_user_category())
    mem.clear()
    print("After clear, length:", len(mem))
