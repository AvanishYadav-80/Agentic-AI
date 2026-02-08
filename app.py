import streamlit as st
from agent import agent_decide
from memory import clear_memory


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
    margin-bottom: 80px; /* space for input bar */
}
</style>
""",
    unsafe_allow_html=True,
)

st.title("🤖 Agentic AI Assistant")

# ---------------- SESSION STATE ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- SIDEBAR ----------------
st.sidebar.title("🧠 Agent Memory")

# ---------------- AGENT SELECTION ----------------
st.sidebar.title("🤖 Choose Agent")

agent_role = st.sidebar.selectbox(
    "Select agent type:", ["Teacher", "Friend", "Doctor", "Engineer"]
)

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
    col1, col2, col3 = st.columns([5, 1, 1])

    with col1:
        user_input = st.text_input(
            "Message input",
            placeholder="Type a message...",
            label_visibility="collapsed",
        )

    with col2:
        submit = st.form_submit_button("➤")

    with col3:
        audio = mic_recorder(start_prompt="🎤", stop_prompt="⏹️", just_once=True)

# ---------------- HANDLE TEXT MESSAGE ----------------
if submit and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.spinner("🤖 Agent is thinking..."):
        response, tool_used = agent_decide(user_input, st.session_state.agent_role)

    st.session_state.messages.append({"role": "assistant", "content": response})

    st.rerun()


# ---------------- VOICE INPUT HANDLING ----------------
if audio and "text" in audio:
    spoken_text = audio["text"]

    st.session_state.messages.append({"role": "user", "content": spoken_text})

    with st.spinner("🤖 Agent is thinking..."):
        response, tool_used = agent_decide(spoken_text, st.session_state.agent_role)

    st.session_state.messages.append({"role": "assistant", "content": response})

    st.rerun()

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown(
    "<center>Made with ❤️ by Avanish Yadav | <a href='https://aboutavi.netlify.app/' target='_blank'>About Me</a></center>",
    unsafe_allow_html=True,
)
