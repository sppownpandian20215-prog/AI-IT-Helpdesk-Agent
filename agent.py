"""
agent.py

ITHelpdeskAgent: the core agent that ties together RAG, tools, and
conversation memory.

Agent workflow:

    User Query
        -> Issue Detection (which category is this?)
        -> RAG Retrieval (what does the knowledge base say?)
        -> Decision Making (do we need a tool? which one?)
        -> Tool Selection
        -> Tool Execution
        -> Memory Update
        -> Final Response
"""

from rag import SimpleRAG, KnowledgeBaseError
from tools import check_network_status, check_system_status, create_support_ticket
from memory import ConversationMemory


# Keyword sets used for simple, transparent issue detection.
# (Kept deliberately simple and rule-based, as required by the project scope.)
CATEGORY_KEYWORDS = {
    "network": ["wifi", "wi-fi", "internet", "network", "router", "connection", "disconnect", "modem"],
    "login": ["password", "login", "log in", "sign in", "account locked", "locked out", "authentication", "mfa"],
    "printer": ["printer", "print", "printing", "toner", "ink", "paper jam"],
    "performance": ["slow", "slowly", "freeze", "freezing", "lag", "performance", "hang", "not responding", "stuck"],
    "software_install": ["install", "installation", "setup.exe", "installer", "won't install", "cannot install"],
    "system_error": ["error", "crash", "crashed", "blue screen", "bsod", "exception", "failure"],
    "escalation": ["not solved", "not resolved", "still not working", "still doesn't work", "need it support",
                   "need support", "escalate", "unresolved", "raise a ticket", "create a ticket",
                   "still isn't working", "doesn't work"],
}

# Human-readable labels for display purposes.
CATEGORY_LABELS = {
    "network": "Network / Wi-Fi Issue",
    "login": "Password / Login Issue",
    "printer": "Printer Issue",
    "performance": "Computer Performance Issue",
    "software_install": "Software Installation Issue",
    "system_error": "System Error",
    "escalation": "IT Support Escalation",
    "unknown": "Unclassified Issue",
}


class ITHelpdeskAgent:
    """
    The agentic controller for the AI IT Helpdesk Agent project.
    Coordinates issue detection, RAG retrieval, tool use, and memory.
    """

    def __init__(self, kb_path: str = None):
        try:
            self.rag = SimpleRAG(kb_path) if kb_path else SimpleRAG()
            self.kb_error = None
        except KnowledgeBaseError as e:
            # Do not crash the whole app if the KB fails to load;
            # degrade gracefully and report the error in responses.
            self.rag = None
            self.kb_error = str(e)

        self.memory = ConversationMemory()

    # ------------------------------------------------------------------
    # Step 1: Issue Detection
    # ------------------------------------------------------------------
    def detect_category(self, query: str) -> str:
        """Rule-based keyword detection of the issue category."""
        text = query.lower()
        for category, keywords in CATEGORY_KEYWORDS.items():
            for kw in keywords:
                if kw in text:
                    return category
        return "unknown"

    # ------------------------------------------------------------------
    # Step 2-4: Decision making / tool selection
    # ------------------------------------------------------------------
    def decide_tool(self, category: str, query: str, follow_up: bool) -> str:
        """
        Decide which tool (if any) should be executed, based on the
        detected category and whether this looks like a follow-up /
        escalation message.
        """
        text = query.lower()

        # Explicit escalation request always creates a ticket.
        if category == "escalation":
            return "ticket"

        # If the user says they already tried the basic fix and it's a
        # follow-up on the same category, escalate instead of repeating.
        if follow_up and any(phrase in text for phrase in
                              ["already restarted", "already tried", "still doesn't work",
                               "still not working", "didn't help", "did not help", "still no"]):
            return "ticket"

        if category == "network":
            return "network_status"
        if category == "performance":
            return "system_status"
        if category == "system_error":
            return "system_status"

        return "none"

    # ------------------------------------------------------------------
    # Main entry point
    # ------------------------------------------------------------------
    def handle_query(self, query: str) -> dict:
        """
        Run the full agent workflow for a single user query.

        Returns a dict containing everything the UI needs to display:
            {
                "category": str,
                "category_label": str,
                "rag_result": dict or None,
                "tool_used": str,
                "tool_result": dict or None,
                "response_text": str,
            }
        """
        if not query or not query.strip():
            return {
                "category": "unknown",
                "category_label": CATEGORY_LABELS["unknown"],
                "rag_result": None,
                "tool_used": "none",
                "tool_result": None,
                "response_text": "Please type a question or describe the issue you're facing "
                                  "so I can help you.",
            }

        query = query.strip()

        # Was the previous user message about the same category?
        # (Simple context/follow-up detection using memory.)
        last_category = self.memory.get_last_user_category()

        # Step 1: Issue Detection
        category = self.detect_category(query)
        effective_category = category if category != "unknown" else (last_category or "unknown")
        is_follow_up = (last_category is not None) and (category in ("unknown", last_category))

        self.memory.add_message("user", query, category=effective_category)

        # Step 2: RAG Retrieval
        rag_result = None
        if self.rag is not None:
            try:
                results = self.rag.retrieve(query, top_k=1)
                rag_result = results[0] if results else None
            except Exception:
                rag_result = None

        # Step 3 & 4: Decision Making + Tool Selection
        tool_used = self.decide_tool(effective_category, query, is_follow_up)

        # Step 5: Tool Execution
        tool_result = None
        try:
            if tool_used == "network_status":
                tool_result = check_network_status()
            elif tool_used == "system_status":
                tool_result = check_system_status()
            elif tool_used == "ticket":
                tool_result = create_support_ticket(query)
        except Exception as e:
            tool_result = {"error": f"Tool execution failed: {e}"}

        # Step 6: Build final response text
        response_text = self._build_response(
            category=effective_category,
            detected_category=category,
            rag_result=rag_result,
            tool_used=tool_used,
            tool_result=tool_result,
            is_follow_up=is_follow_up,
            kb_error=self.kb_error,
        )

        # Step 7: Memory Update (agent side)
        self.memory.add_message("agent", response_text)

        return {
            "category": effective_category,
            "category_label": CATEGORY_LABELS.get(effective_category, CATEGORY_LABELS["unknown"]),
            "rag_result": rag_result,
            "tool_used": tool_used,
            "tool_result": tool_result,
            "response_text": response_text,
        }

    # ------------------------------------------------------------------
    # Response construction
    # ------------------------------------------------------------------
    def _build_response(self, category, detected_category, rag_result, tool_used,
                         tool_result, is_follow_up, kb_error):
        parts = []

        if kb_error:
            parts.append(
                f"⚠️ I couldn't load the knowledge base ({kb_error}). "
                "I can still try to help using available tools."
            )

        # Escalation / ticket path
        if tool_used == "ticket" and tool_result:
            if is_follow_up:
                parts.append(
                    "It looks like the earlier suggestion didn't fully solve the problem. "
                    "Rather than repeat the same steps, I've gone ahead and logged this for "
                    "human IT support."
                )
            else:
                parts.append("I've created a support ticket for this issue so our IT team can assist you.")
            parts.append(
                f"🎫 Ticket ID: **{tool_result.get('ticket_id')}**  |  "
                f"Status: {tool_result.get('status')}  |  Priority: {tool_result.get('priority')}"
            )
            parts.append(f"_Note: {tool_result.get('note')}_")
            return "\n\n".join(parts)

        # Knowledge-base guidance
        if rag_result:
            parts.append(f"**Here's what I found for: {rag_result['category']}**")
            parts.append(rag_result["content"])
        elif detected_category == "unknown" and category == "unknown":
            parts.append(
                "I couldn't find a direct match for this in my knowledge base, so I don't want "
                "to guess and give you incorrect information. This may need a closer look from "
                "our IT support team — let me know if you'd like me to raise a support ticket."
            )
        elif not rag_result:
            parts.append(
                "I recognized this as a possible IT issue, but I couldn't find a strong enough "
                "match in the knowledge base to give you confident guidance."
            )

        # Tool output
        if tool_used == "network_status" and tool_result:
            parts.append(
                f"🔧 **Network Status Tool (Simulated):** {tool_result['status_message']} "
                f"(Wi-Fi connected: {tool_result['wifi_connected']}, "
                f"Internet available: {tool_result['internet_available']}, "
                f"Signal: {tool_result['signal_strength']})"
            )
        elif tool_used == "system_status" and tool_result:
            parts.append(
                f"🔧 **System Status Tool (Simulated):** {tool_result['status_message']} "
                f"(CPU: {tool_result['cpu_usage_percent']}%, "
                f"Memory: {tool_result['memory_usage_percent']}%, "
                f"Free storage: {tool_result['storage_free_gb']} GB)"
            )

        if not parts:
            parts.append(
                "I'm not fully sure how to help with that yet. Could you describe the issue "
                "in a bit more detail, or ask me to raise a support ticket?"
            )

        return "\n\n".join(parts)


if __name__ == "__main__":
    agent = ITHelpdeskAgent()
    test_inputs = [
        "My Wi-Fi is connected but I don't have internet.",
        "My printer is not printing.",
        "My computer is running very slowly.",
        "I forgot my password and cannot login.",
        "My problem is not solved. I need IT support.",
    ]
    for q in test_inputs:
        print("=" * 60)
        print("USER:", q)
        result = agent.handle_query(q)
        print("CATEGORY:", result["category_label"])
        print("TOOL USED:", result["tool_used"])
        print("RESPONSE:\n", result["response_text"])
