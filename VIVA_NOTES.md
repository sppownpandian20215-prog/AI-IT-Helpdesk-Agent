# Viva Notes — AI IT Helpdesk Agent

Simple, student-friendly explanations for your viva / project defense.

---

## What is the project?

It's an AI-powered chatbot that acts like a first-line IT helpdesk. A user
types a problem (like "my Wi-Fi isn't working"), and the app looks up
relevant troubleshooting steps, runs a simulated check (like a network
status check), and gives a combined, helpful answer — while remembering
what was said earlier in the conversation.

## Why did we develop it?

IT helpdesks get a lot of repetitive, simple requests (Wi-Fi, passwords,
printers). This project shows how an AI **agent** can automate the first
response to these common issues, using techniques that don't require an
expensive or external AI API — everything runs locally.

## What is Agentic AI?

Agentic AI means the system doesn't just answer a fixed question — it
**reasons through a sequence of steps and makes decisions**: what kind of
problem is this? What information do I need? Do I need to use a tool?
Should I remember something from earlier? Our agent does all of this in
`agent.py`.

## Where is the agent?

In `agent.py`, in the class `ITHelpdeskAgent`. Its main method,
`handle_query()`, runs the whole pipeline: detect issue → retrieve
knowledge → decide on a tool → run the tool → update memory → build the
final response.

## What is RAG?

RAG stands for **Retrieval-Augmented Generation**. Instead of an AI model
making up an answer from nothing, it first **retrieves** relevant
information from a trusted source (our knowledge base file), and the
final answer is built using that retrieved information. This reduces the
chance of the AI making things up (hallucinating).

## What is TF-IDF?

TF-IDF stands for **Term Frequency – Inverse Document Frequency**. It's a
way to turn text into numbers (a vector) based on how important each word
is. Words that appear a lot in one document but rarely elsewhere get a
higher weight. It lets us compare a user's question to our knowledge base
mathematically.

## What is cosine similarity?

Cosine similarity measures how "close" two vectors point in the same
direction, giving a score from 0 (completely different) to 1 (identical
direction). We use it to compare the TF-IDF vector of the user's question
against the TF-IDF vectors of each knowledge-base section, and pick the
best match.

## What is tool calling?

Tool calling means the AI agent can decide to run a specific function
("tool") to get extra information or perform an action, instead of only
using text knowledge. Our agent can call three tools when needed.

## What are the three tools?

1. **Network Status Tool** — simulates checking Wi-Fi/internet status.
2. **System Status Tool** — simulates checking CPU, memory, and storage.
3. **Support Ticket Tool** — simulates creating an IT support ticket with a unique ticket ID.

## Why are the tools simulated?

Because this is a student prototype without access to real company IT
infrastructure (real routers, servers, or ticketing systems). Simulating
the tools lets us demonstrate the **concept** of tool calling safely and
reliably, without needing real system access or credentials. This is
clearly documented so nobody mistakes it for a production system.

## What is conversation memory?

It's the ability of the agent to remember earlier messages **within the
same chat session**. It's implemented in `memory.py` as a list of
messages with their detected category. This lets the agent notice, for
example, that the user already tried a suggested fix and respond
differently (e.g. escalate) instead of repeating advice.

## Why is Streamlit used?

Streamlit lets us build a clean, working web-based chat interface in pure
Python, very quickly, without needing to write separate frontend
(HTML/CSS/JavaScript) code. It's a common, beginner-friendly choice for AI
project demos.

## What happens when a user enters a query?

1. The query is checked — if it's empty, the agent asks for input.
2. Keywords are checked to detect the issue category (network, login, printer, etc.).
3. The query is compared against the knowledge base using TF-IDF + cosine similarity.
4. The agent decides if a tool should run (e.g. network check for Wi-Fi issues).
5. The tool runs (if selected) and returns a simulated result.
6. The conversation memory is updated with both the user's message and the agent's reply.
7. A combined response (knowledge + tool result) is shown to the user.

## What happens if RAG cannot find an answer?

If the best match's similarity score is below a set threshold (0.08), the
agent does **not** guess. It honestly tells the user it couldn't find a
confident match in the knowledge base, and offers to raise a support
ticket instead — avoiding hallucination.

## What are the limitations?

- Small, static knowledge base — doesn't cover every possible issue.
- Issue detection is keyword-based, not deep semantic understanding.
- All tools are simulated, not connected to real infrastructure.
- Memory only lasts for the current session; nothing is saved permanently.
- Single-user prototype — no login/authentication system.

## What are future enhancements?

- Bigger knowledge base with more categories.
- Smarter, embedding-based semantic search instead of keyword + TF-IDF.
- Persistent storage for chat history and tickets (e.g. a small database).
- Real (permissioned) integrations with actual network/system APIs.
- Optional real LLM integration for more natural, flexible responses.
- User accounts and ticket tracking dashboards.

---

## 1-Minute Project Explanation

"My project is an AI IT Helpdesk Agent — a chatbot that helps with common
IT problems like Wi-Fi, login, printer, and performance issues. It uses a
technique called RAG, where it searches a knowledge base using TF-IDF and
cosine similarity to find the most relevant troubleshooting steps. It also
has three simulated tools — checking network status, checking system
status, and raising a support ticket — which the agent decides to use
based on the type of problem. It remembers the conversation, so if a user
says they already tried a fix, it escalates instead of repeating advice.
Everything runs locally in Python and Streamlit, with no external AI API
required."

## 3-Minute Project Explanation

"My project is called the AI IT Helpdesk Agent, and it's an example of
Agentic AI applied to IT support. The problem I'm addressing is that IT
helpdesks receive a lot of repetitive requests — Wi-Fi problems, forgotten
passwords, printer issues — that could be resolved faster with automated
first-line support.

The system works in a pipeline. First, when a user types a message, the
agent detects what category of issue it might be, using keyword matching
across categories like network, login, printer, performance, software
installation, and system errors. Next, it uses a RAG — Retrieval-Augmented
Generation — approach: the knowledge base is a text file split into
sections, and I use TF-IDF vectorization plus cosine similarity from
scikit-learn to find the most relevant section for the user's question.
This keeps the answers grounded in real, written troubleshooting steps
instead of the AI making things up.

Then, the agent decides if a tool should be used. I built three simulated
tools: a Network Status tool, a System Status tool, and a Support Ticket
tool that generates a unique ticket ID. These are clearly labeled as
simulated because this is a student project without access to real
company infrastructure.

I also added conversation memory, so the agent keeps track of what's been
said in the session. If a user follows up saying they already tried the
suggested fix, the agent recognizes that context and escalates to a
support ticket instead of repeating the same steps.

Finally, everything is wrapped in a Streamlit chat interface, which is
simple to build and lets me demonstrate the whole system visually. The
biggest strength of this project is that it demonstrates all four core
ideas of agentic AI — reasoning, retrieval, tool use, and memory — without
needing any external paid AI API, using only Python and scikit-learn."

---

## 10 Likely Viva Questions & Simple Answers

1. **Q: Why didn't you use a real LLM like GPT or Claude?**
   A: The project scope required it to work without an external API key, to keep it free, simple, and reliable for a student demo. TF-IDF + cosine similarity + rule-based logic is enough to demonstrate the core agentic AI concepts.

2. **Q: How does your agent decide which tool to call?**
   A: Based on the detected issue category and conversation context — e.g. network issues trigger the Network Status tool, performance/system-error issues trigger the System Status tool, and explicit escalation or repeated unresolved issues trigger the Support Ticket tool.

3. **Q: What happens if the user's question isn't in the knowledge base?**
   A: The cosine similarity score will be below our threshold (0.08), so the agent won't return a low-confidence guess — it tells the user honestly and offers to escalate.

4. **Q: Is this connected to a real company network or ticketing system?**
   A: No. All tools are clearly simulated in `tools.py` and generate realistic but fake results, purely for demonstration.

5. **Q: How is conversation memory implemented?**
   A: As an in-session Python list of message dictionaries (`memory.py`), storing role, message text, category, and timestamp. It's not saved permanently — it resets when the session/app restarts.

6. **Q: What is the difference between TF-IDF and just keyword matching?**
   A: Keyword matching only checks if exact words appear. TF-IDF converts text into weighted numeric vectors, factoring in how important/rare a word is, so it can better compare overall similarity between the user query and each knowledge base entry — not just exact word overlap.

7. **Q: How do you avoid the AI hallucinating (making up wrong answers)?**
   A: By using RAG — the agent only ever returns content taken directly from theknowledge base file, and only if the similarity score passes a minimum threshold. It never generates free-form text answers about troubleshooting steps.

8. **Q: What would you need to make this production-ready?**
   A: Replace the simulated tools with real, permissioned API integrations; add authentication; add persistent storage for chats/tickets; expand the knowledge base; and possibly integrate a real LLM for more natural conversation while keeping RAG for grounding.

9. **Q: Why did you choose Streamlit for the UI?**
   A: It lets you build an interactive web UI purely in Python very quickly, which is ideal for demoing an AI prototype without needing separate frontend development skills.

10. **Q: How did you test the project?**
    A: I ran each core module (`rag.py`, `tools.py`, `memory.py`, `agent.py`) standalone to verify their logic, checked all files for syntax errors, and manually walked through all 7 required test cases end-to-end using the agent's `handle_query()` function, confirming the expected category, tool, and response for each. See `TESTING.md` for full details.
