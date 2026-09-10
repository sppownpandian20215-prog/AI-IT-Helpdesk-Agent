# AI IT Helpdesk Agent: An Intelligent Troubleshooting Assistant

A college-level **Agentic AI** internship project that demonstrates an AI-powered
IT helpdesk assistant combining **Agentic AI**, **Retrieval-Augmented Generation
(RAG)**, **Tool Calling**, **Conversation Memory**, and a **Streamlit** chat UI —
built entirely with Python and scikit-learn, with **no external LLM API required**.

---

## 1. Project Overview

The AI IT Helpdesk Agent simulates a first-line IT support assistant. A user
describes a technical problem (Wi-Fi, login, printer, performance, software
installation, or a system error) in plain English, and the agent:

1. Detects what kind of issue it is.
2. Retrieves the most relevant troubleshooting guidance from a local knowledge base using TF-IDF + cosine similarity (RAG).
3. Decides whether a supporting tool should be run (e.g. a simulated network check).
4. Executes that tool.
5. Remembers the conversation so it can respond intelligently to follow-up messages.
6. Returns a combined, human-readable response.

## 2. Problem Statement

IT support desks receive a large volume of repetitive, low-complexity
requests (Wi-Fi issues, password resets, printer problems, etc.). Human
agents spend significant time on issues that could be resolved instantly
with the right documented steps. This project explores how an **agentic**
AI system — one that reasons about a request, retrieves relevant
knowledge, and decides which actions/tools to invoke — can automate this
first line of support in a transparent, explainable way.

## 3. Objectives

- Build a working agentic AI system without relying on a paid/external LLM API.
- Demonstrate RAG using classical NLP techniques (TF-IDF + cosine similarity).
- Demonstrate tool calling with simulated IT tools.
- Demonstrate conversation memory that lets the agent use context from earlier messages.
- Package everything behind a simple, usable Streamlit chat interface.

## 4. Features

- 💬 Conversational chat interface (Streamlit `st.chat_message` / `st.chat_input`).
- 📚 RAG-based retrieval over a local knowledge base (`knowledge_base/troubleshooting.txt`).
- 🧠 Rule-based issue/category detection (network, login, printer, performance, software install, system error, escalation).
- 🔧 Three simulated tools: Network Status, System Status, Support Ticket.
- 🧵 In-session conversation memory that lets the agent recognize follow-up messages (e.g. "I already restarted the router").
- 🛡️ Graceful error handling for empty input, missing knowledge base, and tool/retrieval failures.
- 🗑️ "Clear Chat" button to reset the session.

## 5. Technologies Used

| Category            | Technology                              |
|---------------------|------------------------------------------|
| Language             | Python 3.10+                            |
| UI Framework         | Streamlit                               |
| RAG / NLP            | scikit-learn (`TfidfVectorizer`, `cosine_similarity`) |
| Memory               | Plain Python data structures (in-session) |
| Tools                | Simulated Python functions              |
| LLM / External API   | **None** — not required for this project |

## 6. System Architecture

```
                ┌─────────────────────┐
                │   Streamlit UI       │  app.py
                │  (chat interface)    │
                └──────────┬───────────┘
                           │ user query
                           ▼
                ┌─────────────────────┐
                │  ITHelpdeskAgent      │  agent.py
                │  (agentic controller) │
                └──────┬───────┬───────┘
                       │       │
          ┌────────────┘       └─────────────┐
          ▼                                   ▼
 ┌────────────────────┐             ┌───────────────────┐
 │   SimpleRAG          │             │  Tools              │
 │   (TF-IDF + cosine)  │             │  (Network / System / │
 │   rag.py              │             │   Support Ticket)   │
 └──────────┬──────────┘             └───────────────────┘
            │
            ▼
 ┌────────────────────┐
 │ knowledge_base/      │
 │ troubleshooting.txt  │
 └────────────────────┘

          ▲
          │
 ┌────────────────────┐
 │ ConversationMemory   │  memory.py
 │ (session history)    │
 └────────────────────┘
```

## 7. Agentic AI Workflow

```
User Query
    ↓
Issue Detection      (keyword-based category classification)
    ↓
RAG Retrieval         (TF-IDF + cosine similarity over knowledge base)
    ↓
Decision Making        (does this need a tool? which one?)
    ↓
Tool Selection          (network / system / ticket / none)
    ↓
Tool Execution          (simulated result)
    ↓
Memory Update           (store user + agent turns)
    ↓
Final Response          (combined RAG + tool output)
```

The agent is implemented in `agent.py` as the `ITHelpdeskAgent` class. It is
"agentic" in the sense that it does not simply return a static lookup —
it reasons over the detected category, conversation history (has the user
already tried the suggested fix?), and decides for itself whether to invoke
a tool and which one, rather than a human hard-coding that decision per query.

## 8. RAG Implementation

- The knowledge base (`knowledge_base/troubleshooting.txt`) is split into
  chunks, one per `CATEGORY:` section.
- Each chunk is converted into a TF-IDF vector using scikit-learn's
  `TfidfVectorizer`.
- A user's query is vectorized with the same vectorizer, and **cosine
  similarity** is computed between the query and every chunk.
- The highest-scoring chunk is returned **only if** its score is above a
  minimum threshold (`SIMILARITY_THRESHOLD = 0.08`); otherwise the agent
  honestly reports that it could not find a confident match, instead of
  hallucinating an answer.

## 9. Tool Calling

Three tools are implemented in `tools.py`. **All three are simulated** —
none of them access real hardware, real networks, or a real ticketing
system. This is intentional and is required by the project scope.

| Tool | Purpose | Simulated Output |
|------|---------|-------------------|
| Network Status Tool | Simulates checking Wi-Fi / internet status | Wi-Fi connected (bool), internet available (bool), signal strength |
| System Status Tool | Simulates checking system health | CPU %, memory %, free storage (GB) |
| Support Ticket Tool | Simulates raising an IT ticket | Unique ticket ID (e.g. `IT-20260909123045`), issue, status |

The agent decides which tool (if any) to call based on the detected issue
category and conversation context (see `ITHelpdeskAgent.decide_tool`).

## 10. Conversation Memory

`memory.py` implements `ConversationMemory`, a simple in-session store with:

- `add_message(role, message, category)`
- `get_history()`
- `get_recent_messages(n)`
- `get_last_user_category()`
- `clear()`

This lets the agent recognize, for example, that "I already restarted the
router but it still doesn't work" is a **follow-up** to a previous Wi-Fi
question, and respond by escalating to a support ticket instead of
repeating the same troubleshooting steps.

## 11. Project Structure

```
AI-IT-Helpdesk-Agent/
│
├── knowledge_base/
│   └── troubleshooting.txt
│
├── agent.py
├── app.py
├── memory.py
├── rag.py
├── tools.py
├── requirements.txt
├── README.md
├── TESTING.md
├── VIVA_NOTES.md
├── .gitignore
│
└── report/
    └── project_report.md
```

## 12. Installation

```bash
# 1. Clone or download the project, then move into the folder
cd AI-IT-Helpdesk-Agent

# 2. (Recommended) create a virtual environment
python -m venv venv

# Activate it:
# Windows:
venv\Scripts\activate
# macOS / Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

## 13. How to Run

```bash
python -m streamlit run app.py
```

Streamlit will open the app in your browser (typically at
`http://localhost:8501`). If it doesn't open automatically, copy the URL
shown in the terminal into your browser.

## 14. Example Queries

Try typing these into the chat box:

1. `My Wi-Fi is connected but I don't have internet.`
2. `My printer is not printing.`
3. `My computer is running very slowly.`
4. `I forgot my password and cannot login.`
5. `My problem is not solved. I need IT support.`
6. `I already restarted my router but the Wi-Fi still doesn't work.` (as a follow-up to #1)
7. `My laptop has an unknown problem that isn't in the knowledge base.`

## 15. Limitations

- The knowledge base is a small, static text file — it does not cover every possible IT issue.
- Issue detection uses simple keyword matching, not deep semantic understanding.
- All tools are **simulated**; no real network, system, or ticketing infrastructure is contacted.
- Conversation memory only lasts for the current Streamlit session (it is not saved permanently).
- No authentication or multi-user support — this is a single-user prototype/demo.

## 16. Future Enhancements

- Expand the knowledge base with more categories and more detailed steps.
- Add a real embeddings-based retriever for better semantic matching.
- Persist conversation history and tickets to a lightweight database.
- Connect the tools to real (permissioned) system/network APIs in a production setting.
- Add user authentication and per-user ticket tracking.
- Optionally integrate a real LLM for more natural free-form responses.

## 17. Conclusion

This project demonstrates, at a scope appropriate for a college internship,
how the core ideas of agentic AI systems — retrieval, reasoning, tool use,
and memory — can be combined into a working, explainable, locally-runnable
application without dependency on external LLM APIs. It is intended as a
learning and demonstration project, not a production IT support system.
