# ui.py
import streamlit as st
from main import process_query, summarize_chat

st.set_page_config(page_title="Atgeir Intranet Chatbot", page_icon="🤖")

# Style
st.markdown(
    """
    <style>
    .st-emotion-cache-1r6slb0, .stApp {
        background: linear-gradient(to right, #ffafbd, #ffc3a0);
        color: #333 !important; /* Dark gray for better contrast */
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

    .bot-eye.left {
        left: 12px;
        animation: bot-blink 4s infinite;
    }

    .bot-eye.right {
        right: 12px;
        animation: bot-blink 4s infinite 0.2s;
    }

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
   
    @keyframes pulse-bg {
        0% { opacity: 0.8; transform: scale(1); }
        50% { opacity: 1; transform: scale(1.05); }
        100% { opacity: 0.8; transform: scale(1); }
    }

    @keyframes float-particles {
        0% { transform: translateY(0) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(5deg); }
        100% { transform: translateY(0) rotate(0deg); }
    }

    @keyframes bot-float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }

    @keyframes bot-blink {
        0%, 45%, 55%, 100% { height: 12px; }
        50% { height: 2px; }
    }

    @keyframes bot-talk {
        0%, 100% { width: 25px; height: 5px; }
        50% { width: 35px; height: 8px; }
    }

    @keyframes bot-glow {
        0%, 100% { background-color: #34d399; box-shadow: 0 0 10px #34d399; }
        50% { background-color: #10b981; box-shadow: 0 0 20px #10b981; }
    }

    @keyframes text-shimmer {
        0% { background-position: -100% 0; }
        100% { background-position: 200% 0; }
    }
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
    </style>
    """,
    unsafe_allow_html=True
)

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

    query = st.text_input("Ask me a question:", "")
    if st.button("Send") and query:
        response = process_query(query)
        st.write(f"**Assistant:** {response}")

    if st.button("View Chat History"):
        st.write("### Conversation History")
        for msg in st.session_state.messages:
            icon = "👤" if msg["role"] == "user" else "🤖"
            st.write(f"{icon} **{msg['role'].capitalize()}**: {msg['content']}")

    if st.button("View Chat Summary"):
        summary = summarize_chat(st.session_state.messages)
        st.write("### Chat Summary")
        st.write(summary)
    if st.button("Explore more Chatbots", key="more_chatbots", use_container_width=True):
        st.session_state.page = "more_chatbots"
        st.rerun()      
# Blank Page for More Chatbots
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
            height: 100vh;  /* Full-screen chatbot */
            border-radius: 0px;
            box-shadow: none;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Using an iframe to embed Dialogflow Messenger for better interactivity
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)

    # Using an iframe to embed Dialogflow Messenger for better interactivity
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
    st.markdown('</div>', unsafe_allow_html=True)

    # Button to go back to upload page
    st.markdown('<div style="margin-bottom: 0px;">', unsafe_allow_html=True)
    if st.button("⬅ Back to Chatbot"):
        st.session_state.page = "chatbot"
        st.rerun()
