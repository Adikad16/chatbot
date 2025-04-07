# ui.py

import streamlit as st
from main import process_query, summarize_chat

st.set_page_config(page_title="Atgeir Intranet Chatbot", page_icon="🤖")

# ===============================
# Custom Styles and Bot Animation
# ===============================
st.markdown(
    """
    <style>
    .st-emotion-cache-1r6slb0, .stApp {
        background: linear-gradient(to right, #ffafbd, #ffc3a0);
        color: #333 !important;
        overflow: auto;
    }

    .animated-bot {
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 80px;
        height: 80px;
        z-index: 1000;
        pointer-events: none;
    }

    .bot-head {
        position: absolute;
        width: 60px;
        height: 60px;
        background: linear-gradient(135deg, #10b981, #3b82f6);
        border-radius: 15px;
        top: 0;
        left: 10px;
        animation: bot-float 3s ease-in-out infinite;
        box-shadow: 0 10px 25px rgba(16, 185, 129, 0.3);
    }

    .bot-eye {
        position: absolute;
        width: 12px;
        height: 12px;
        background-color: white;
        border-radius: 50%;
        top: 15px;
    }

    .bot-eye.left { left: 12px; animation: bot-blink 4s infinite; }
    .bot-eye.right { right: 12px; animation: bot-blink 4s infinite 0.2s; }

    .bot-mouth {
        position: absolute;
        width: 25px;
        height: 5px;
        background-color: white;
        border-radius: 3px;
        bottom: 15px;
        left: 50%;
        transform: translateX(-50%);
        animation: bot-talk 3s infinite;
    }

    .bot-antenna {
        position: absolute;
        width: 6px;
        height: 15px;
        background-color: #10b981;
        top: -15px;
        left: 50%;
        transform: translateX(-50%);
        border-radius: 3px;
    }

    .bot-antenna-bulb {
        position: absolute;
        width: 10px;
        height: 10px;
        background-color: #34d399;
        border-radius: 50%;
        top: -25px;
        left: 50%;
        transform: translateX(-50%);
        animation: bot-glow 2s infinite;
        box-shadow: 0 0 10px #34d399;
    }

    .chat-instruction {
        text-align: center;
        font-size: 36px;
        font-weight: bold;
        margin: 10px auto;
        color: #333;
    }

    div.stButton > button {
        font-size: 24px;
        font-weight: bold;
        border-radius: 0.5em;
        padding: 0.7em 1.7em;
        width: 100%;
    }

    @keyframes bot-float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-10px); } }
    @keyframes bot-blink { 0%, 45%, 55%, 100% { height: 12px; } 50% { height: 2px; } }
    @keyframes bot-talk { 0%, 100% { width: 25px; height: 5px; } 50% { width: 35px; height: 8px; } }
    @keyframes bot-glow { 0%, 100% { background-color: #34d399; box-shadow: 0 0 10px #34d399; }
                          50% { background-color: #10b981; box-shadow: 0 0 20px #10b981; } }
    </style>

    <div class="animated-bot">
        <div class="bot-head">
            <div class="bot-eye left"></div>
            <div class="bot-eye right"></div>
            <div class="bot-mouth"></div>
            <div class="bot-antenna"></div>
            <div class="bot-antenna-bulb"></div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ===============================
# Page Navigation
# ===============================

if "page" not in st.session_state:
    st.session_state.page = "welcome"

if st.session_state.page == "welcome":
    st.markdown('<div class="chat-instruction">Welcome to Atgeir Intranet Chatbot</div>', unsafe_allow_html=True)
    st.markdown('<div class="chat-instruction"><p>Interact with documents seamlessly.</p></div>', unsafe_allow_html=True)

    if st.button("Chat", key="chatbot", use_container_width=True):
        st.session_state.page = "chatbot"
        st.rerun()

elif st.session_state.page == "chatbot":
    st.markdown('<div class="chat-instruction">📄 Document Q&A Chatbot</div>', unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display existing chat
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat Input
    user_input = st.chat_input("Type your question here...")
    if user_input:
        with st.spinner("Thinking..."):
            
            response = process_query(user_input)

        with st.chat_message("user"):
            st.markdown(user_input)
        with st.chat_message("assistant"):
            st.markdown(response)

    # Chat History
    if st.button("📜 View Chat History"):
        st.subheader("Conversation History")
        for msg in st.session_state.messages:
            icon = "👤" if msg["role"] == "user" else "🤖"
            st.markdown(f"{icon} **{msg['role'].capitalize()}**: {msg['content']}")

    # Chat Summary
    if st.button("📝 Summarize Chat"):
        with st.spinner("Summarizing..."):
            summary = summarize_chat(st.session_state.messages)
        st.subheader("Chat Summary")
        st.markdown(summary)

    if st.button("🤖 Explore more Chatbots", key="more_chatbots", use_container_width=True):
        st.session_state.page = "more_chatbots"
        st.rerun()

elif st.session_state.page == "more_chatbots":
    st.markdown('<div class="chat-instruction">🤖 Explore More Chatbots</div>', unsafe_allow_html=True)

    st.markdown(
        """
        <style>
        df-messenger {
            z-index: 999;
            position: fixed;
            bottom: 0px;
            right: 0px;
            width: 100%;
            height: 100vh;
            border-radius: 0px;
            box-shadow: none;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    chatbot_url = "https://www.gstatic.com/dialogflow-console/fast/df-messenger/prod/v1/df-messenger.js"
    chatbot_html = f"""
    <script src="{chatbot_url}"></script>
    <df-messenger
      project-id="mini-project-454908"
      agent-id="7ac4404c-0290-4ee6-b5bd-3b5d88b7a497"
      language-code="en">
    </df-messenger>
    """

    st.components.v1.html(chatbot_html, height=575)

    if st.button("⬅ Back to Chatbot"):
        st.session_state.page = "chatbot"
        st.rerun()
