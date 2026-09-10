"""
tools.py
--------
Simulated tools available to the AI IT Helpdesk Agent.

IMPORTANT (for the report and viva):
All tools in this file are SIMULATED. None of them connect to any real
network hardware, real operating system internals, or a real ticketing
system. They generate realistic-looking but randomly/deterministically
simulated results purely for demonstration purposes in this student
project. This is clearly documented here and in the README.
"""

import random
import uuid
from datetime import datetime


def check_network_status() -> dict:
    """
    TOOL 1 — Network Status Tool (SIMULATED)

    Simulates checking Wi-Fi connection, internet availability, and
    general network status. Does NOT perform any real network requests.
    """
    wifi_connected = random.choice([True, True, False])  # mostly connected, for demo variety
    internet_available = random.choice([True, False]) if wifi_connected else False
    signal_strength = random.choice(["Excellent", "Good", "Weak", "Very Weak"])

    if wifi_connected and internet_available:
        status = "Wi-Fi connected and internet is reachable."
    elif wifi_connected and not internet_available:
        status = "Wi-Fi connected, but internet is NOT reachable (possible router/ISP issue)."
    else:
        status = "Wi-Fi is not connected."

    return {
        "tool": "Network Status Tool (Simulated)",
        "wifi_connected": wifi_connected,
        "internet_available": internet_available,
        "signal_strength": signal_strength,
        "status_message": status,
        "checked_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


def check_system_status() -> dict:
    """
    TOOL 2 — System Status Tool (SIMULATED)

    Simulates checking basic system health: CPU load, memory usage,
    and storage usage. Does NOT read any real system metrics.
    """
    cpu_usage = random.randint(20, 95)
    memory_usage = random.randint(30, 95)
    storage_free_gb = random.randint(5, 250)

    if cpu_usage > 85 or memory_usage > 85:
        condition = "System is under heavy load. This may be causing slowness."
    elif storage_free_gb < 10:
        condition = "Storage is critically low. This may be causing slowness or errors."
    else:
        condition = "System resources look normal."

    return {
        "tool": "System Status Tool (Simulated)",
        "cpu_usage_percent": cpu_usage,
        "memory_usage_percent": memory_usage,
        "storage_free_gb": storage_free_gb,
        "status_message": condition,
        "checked_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


def create_support_ticket(issue_description: str) -> dict:
    """
    TOOL 3 — Support Ticket Tool (SIMULATED)

    Simulates creating an IT support ticket and generates a unique
    ticket ID. Does NOT create a ticket in any real ticketing system.
    """
    if not issue_description or not issue_description.strip():
        issue_description = "Unspecified issue reported by user."

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    ticket_id = f"IT-{timestamp}"

    return {
        "tool": "Support Ticket Tool (Simulated)",
        "ticket_id": ticket_id,
        "issue": issue_description.strip(),
        "status": "Open",
        "priority": "Normal",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "note": "This is a SIMULATED ticket for demonstration purposes only. "
                "No real IT support system has been contacted.",
    }


if __name__ == "__main__":
    print(check_network_status())
    print(check_system_status())
    print(create_support_ticket("Wi-Fi connected but no internet access."))
