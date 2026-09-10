# Testing Document — AI IT Helpdesk Agent

## How testing was performed

The build environment used to create this project **could not install or
launch Streamlit itself** (no internet access in that sandbox to `pip
install streamlit`), so the full graphical chat interface could not be
click-tested end-to-end in that environment.

However, all of the "brains" of the agent — **RAG retrieval (`rag.py`),
tools (`tools.py`), conversation memory (`memory.py`), and the full agent
workflow (`agent.py`)** — are plain Python modules with **no Streamlit
dependency**, so they were executed and verified directly, including all
7 required test cases below, via:

```bash
python3 rag.py
python3 tools.py
python3 memory.py
python3 agent.py
```

All Python files (including `app.py`) were also checked for syntax errors
with:

```bash
python3 -m py_compile app.py agent.py rag.py tools.py memory.py
```
Result: **all files compiled successfully, no syntax errors.**

`app.py` itself is a thin UI layer that calls `ITHelpdeskAgent.handle_query()`
(the same function verified below) and displays the result — it does not
contain separate business logic. Because of this, the backend test results
below give strong confidence the UI will behave correctly, but you should
still run `python -m streamlit run app.py` yourself and click through the
scenarios once, since the actual rendered UI was not visually inspected by
the assistant.

## Test Case Table

| Test Case ID | User Input | Expected Result | Status |
|---|---|---|---|
| TC-01 | "My Wi-Fi is connected but I don't have internet." | Relevant Wi-Fi troubleshooting info retrieved from KB, and Network Status tool result shown. | **Passed** (verified via `python3 agent.py` — category = network, tool = network_status, KB match score 0.669) |
| TC-02 | "My printer is not printing." | Relevant printer troubleshooting information returned. | **Passed** (category = printer, KB match score 0.626) |
| TC-03 | "My computer is running very slowly." | Relevant performance troubleshooting info and System Status tool result shown. | **Passed** (category = performance, tool = system_status, KB match score 0.220) |
| TC-04 | "I forgot my password and cannot login." | Relevant password/login troubleshooting information returned. | **Passed** (category = login, KB match score 0.425) |
| TC-05 | "My problem is not solved. I need IT support." | Support Ticket tool triggered; a ticket ID is generated. | **Passed** (tool = ticket, ticket ID generated in format `IT-YYYYMMDDHHMMSS`) |
| TC-06 | "I already restarted my router but the Wi-Fi still doesn't work." (sent as a follow-up after a Wi-Fi question in the same session) | Agent uses conversation context and recommends the next step (escalation) instead of repeating the same advice. | **Passed** (verified with a scripted 2-turn conversation: first turn detected as `network` with the network tool run; second turn recognized as a follow-up and automatically escalated to a support ticket) |
| TC-07 | "My laptop has an unknown problem that isn't in the knowledge base." | Agent clearly states it could not find a direct solution, and suggests escalation. | **Passed** (category = unknown, no RAG match above threshold, response explicitly states no confident match was found and offers to raise a ticket) |

## Additional checks performed

| Check | Result |
|---|---|
| Empty query submitted | **Passed** — agent returns a friendly prompt asking the user to type a message, instead of crashing. |
| Knowledge base file missing/renamed | **Passed** — `SimpleRAG` raises a clear `KnowledgeBaseError`; `ITHelpdeskAgent` catches it, stores the message, and still allows tools (network/system status) to work rather than crashing the whole app. |
| Invalid/failed tool call (simulated exception) | **Handled** — tool execution is wrapped in a `try/except` in `agent.py`; a failure returns an error dict rather than crashing. |
| Python syntax / imports across all files | **Passed** — `python3 -m py_compile` succeeded on all 5 `.py` files. |

## What is marked "To Be Tested"

| Item | Status |
|---|---|
| Full Streamlit UI, visually, in a real browser (chat bubbles rendering, sidebar layout, Clear Chat button click) | **To Be Tested** by you, in your own environment, since the assistant's sandbox could not install Streamlit. Run `python -m streamlit run app.py` and click through TC-01 to TC-07 to confirm. |
| Behavior across different terminal/OS/Python patch versions | **To Be Tested** — developed and logic-tested on Python 3.12. |

## How to re-run these tests yourself

```bash
# Backend/module tests (no Streamlit needed)
python3 rag.py
python3 tools.py
python3 memory.py
python3 agent.py

# Full UI test
python -m streamlit run app.py
# Then manually type each TC-01..TC-07 input into the chat box.
```
