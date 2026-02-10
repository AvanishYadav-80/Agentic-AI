import streamlit as st
from agent import agent_decide
from memory import clear_memory

# st.cache_data.clear()
# st.cache_resource.clear()

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Agentic AI Assistant", page_icon="🤖", layout="centered")

# ---------------- CUSTOM CSS ----------------
st.markdown(
    """
<style>
.chat-user {
    background-color: #DCF8C6;
    color: black;
    padding: 10px 14px;
    border-radius: 18px;
    max-width: 45%;
    margin-left: auto;
    margin-bottom: 10px;
}

.chat-agent {
    background-color: #2B2B2B;
    color: white;
    padding: 10px 14px;
    border-radius: 18px;
    max-width: 75%;
    margin-right: auto;
    margin-bottom: 10px;
}

.chat-container {
    display: flex;
    flex-direction: column;
    margin-bottom: 80px; /* space for input bar */`1
}


/* ---------- GLOBAL MOBILE FIX ---------- */
html, body {
    font-size: 16px;
}

/* Remove Streamlit extra padding */
.block-container {
    padding: 1rem 0.8rem 5rem 0.8rem;
}

/* ---------- CHAT CONTAINER ---------- */
.chat-container {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

/* ---------- USER MESSAGE (RIGHT SIDE) ---------- */
.chat-user {
    align-self: flex-end;
    background-color: #DCF8C6;
    color: #000;
    padding: 8px 12px;
    border-radius: 18px 18px 4px 18px;

    width: fit-content;
    max-width: 75%;

    word-wrap: break-word;
    white-space: pre-wrap;
    font-size: 15px;
}

/* ---------- AGENT MESSAGE (LEFT SIDE) ---------- */
.chat-agent {
    align-self: flex-start;
    background-color: #2B2B2B;
    color: #fff;
    padding: 8px 12px;
    border-radius: 18px 18px 18px 4px;

    width: fit-content;
    max-width: 75%;

    word-wrap: break-word;
    white-space: pre-wrap;
    font-size: 15px;
}

/* ---------- INPUT AREA ---------- */
form {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: #ffffff;
    padding: 8px 10px;
    border-top: 1px solid #ddd;
    z-index: 100;
}

/* Make input box rounded */
input[type="text"] {
    border-radius: 20px !important;
    padding: 10px !important;
}

/* Send button style */
button[kind="primary"] {
    border-radius: 50%;
    height: 42px;
    width: 42px;
    padding: 0;
}

/* ---------- MOBILE RESPONSIVE ---------- */
@media (max-width: 600px) {

    .chat-user,
    .chat-agent {
        max-width: 90%;
        font-size: 14px;
    }

    form {
        padding: 6px 8px;
    }
}

</style>
""",
    unsafe_allow_html=True,
)

st.title("🤖 Agentic AI Assistant")

# ---------------- SESSION STATE ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "agent_role" not in st.session_state:
    st.session_state.agent_role = "Friend"


# ---------------- SIDEBAR ----------------
st.sidebar.title("🧠 Agent Memory")

# ---------------- AGENT SELECTION ----------------
st.sidebar.title("🤖 Choose Agent")

agent_role = st.sidebar.selectbox(
    "Select agent type:", ["Teacher", "Friend", "Doctor", "Engineer"]
)
AGENT_DESCRIPTIONS = {
    "Teacher": "📘 Explains concepts step-by-step with simple examples.",
    "Friend": "😊 Casual, friendly conversation partner.",
    "Doctor": "🩺 Provides general health information (not diagnosis).",
    "Engineer": "💻 Technical, precise, problem-solving focused."
}

st.sidebar.info(AGENT_DESCRIPTIONS[st.session_state.agent_role])


# Store selected agent in session
if "agent_role" not in st.session_state:
    st.session_state.agent_role = agent_role

# If user changes agent, reset memory
if agent_role != st.session_state.agent_role:
    st.session_state.agent_role = agent_role
    st.session_state.messages = []
    clear_memory()
    st.rerun()


if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    clear_memory()
    st.rerun()

if st.session_state.messages:
    for msg in st.session_state.messages:
        st.sidebar.markdown(f"**{msg['role'].capitalize()}**: {msg['content']}")
else:
    st.sidebar.write("No memory yet.")

# ---------------- CHAT HISTORY ----------------
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(
            f'<div class="chat-user">{msg["content"]}</div>', unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<div class="chat-agent">{msg["content"]}</div>', unsafe_allow_html=True
        )

st.markdown("</div>", unsafe_allow_html=True)


# ---------------- INPUT SECTION (ENTER + SEND WORKS) ----------------
audio = None  # ✅ important

with st.form("chat_form", clear_on_submit=True):
    col1, col2 = st.columns([6, 1])

    with col1:
        user_input = st.text_input(
            "Message input",
            placeholder="Type a message...",
            label_visibility="collapsed",
        )

    with col2:
        submit = st.form_submit_button("➤")
        

# ---------------- HANDLE TEXT MESSAGE ----------------
if submit and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    MAX_MESSAGES = 10
    st.session_state.messages = st.session_state.messages[-MAX_MESSAGES:]


    with st.spinner("🤖 Agent is thinking..."):
        response, tool_used = agent_decide(user_input, st.session_state.agent_role)

        if tool_used:
            st.caption(f"🛠️ Tool used: `{tool_used}`")


    st.session_state.messages.append({"role": "assistant", "content": response})

    MAX_MESSAGES = 10
    st.session_state.messages = st.session_state.messages[-MAX_MESSAGES:]


    st.rerun()


# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown(
    "<center>Made with ❤️ by Avanish Yadav | <a href='https://aboutavi.netlify.app/' target='_blank'>About Me</a></center>",
    unsafe_allow_html=True,
)
