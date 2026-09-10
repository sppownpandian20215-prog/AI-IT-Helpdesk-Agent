"""
app.py
------
Streamlit UI for the AI IT Helpdesk Agent.

Run with:
    python -m streamlit run app.py
"""

import streamlit as st
from agent import ITHelpdeskAgent

st.set_page_config(
    page_title="AI IT Helpdesk Agent",
    page_icon="🖥️",
    layout="centered",
)


# ----------------------------------------------------------------------
# Session state initialization
# ----------------------------------------------------------------------
if "agent" not in st.session_state:
    try:
        st.session_state.agent = ITHelpdeskAgent()
    except Exception as e:
        st.session_state.agent = None
        st.session_state.init_error = str(e)

if "chat_display" not in st.session_state:
    st.session_state.chat_display = []  # list of {"role": ..., "content": ...} for rendering


# ----------------------------------------------------------------------
# Sidebar
# ----------------------------------------------------------------------
with st.sidebar:
    st.header("Project")
    st.markdown("**AI IT Helpdesk Agent**")
    st.caption("An Intelligent Troubleshooting Assistant (Agentic AI Internship Project)")

    st.divider()
    st.subheader("Technologies")
    st.markdown(
        "- Python\n"
        "- Streamlit\n"
        "- scikit-learn\n"
        "- TF-IDF\n"
        "- Cosine Similarity\n"
        "- RAG (Retrieval-Augmented Generation)\n"
        "- Tool Calling\n"
        "- Conversation Memory"
    )

    st.divider()
    st.subheader("Knowledge Base Covers")
    st.markdown(
        "- Wi-Fi & Internet\n"
        "- Login / Password\n"
        "- Printer\n"
        "- Computer Performance\n"
        "- Software Installation\n"
        "- System Errors"
    )

    st.divider()
    st.subheader("Tools (Simulated)")
    st.markdown(
        "- 🌐 Network Status\n"
        "- 🖥️ System Status\n"
        "- 🎫 Support Ticket"
    )
    st.caption("All tools are simulated for demonstration. No real IT infrastructure is accessed.")

    st.divider()
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.chat_display = []
        if st.session_state.agent is not None:
            st.session_state.agent.memory.clear()
        st.rerun()


# ----------------------------------------------------------------------
# Main page
# ----------------------------------------------------------------------
st.title("🖥️ AI IT Helpdesk Agent")
st.write(
    "An intelligent troubleshooting assistant that combines **Agentic AI**, "
    "**Retrieval-Augmented Generation (RAG)**, **Tool Calling**, and "
    "**Conversation Memory** to help resolve common IT issues — Wi-Fi, login, "
    "printer, performance, installation, and system errors."
)
st.info(
    "ℹ️ This is a student prototype. Network/system checks and support-ticket "
    "creation are **simulated** and do not connect to any real IT infrastructure.",
    icon="ℹ️",
)

if st.session_state.agent is None:
    st.error(f"The agent could not start: {st.session_state.get('init_error')}")
    st.stop()

if st.session_state.agent.kb_error:
    st.warning(f"Knowledge base issue: {st.session_state.agent.kb_error}")

# Render existing chat history
for msg in st.session_state.chat_display:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
user_input = st.chat_input("Describe your IT problem (e.g. 'My Wi-Fi is connected but I have no internet')")

if user_input is not None:
    # Guard against accidental empty submissions
    if not user_input.strip():
        st.warning("Please type a message before sending.")
    else:
        st.session_state.chat_display.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        try:
            result = st.session_state.agent.handle_query(user_input)
            response_text = result["response_text"]
        except Exception as e:
            response_text = (
                f"⚠️ Something went wrong while processing your request: {e}\n\n"
                "Please try rephrasing your question, or clear the chat and try again."
            )

        st.session_state.chat_display.append({"role": "assistant", "content": response_text})
        with st.chat_message("assistant"):
            st.markdown(response_text)
