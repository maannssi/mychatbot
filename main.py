import streamlit as st
from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage, HumanMessage
from dotenv import load_dotenv
import os
from uuid import uuid4
from streamlit import session_state as state
from file_uploads import handle_pdf_upload, handle_image_upload

# Load API key
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

# App config
st.set_page_config(page_title="GPT Clone", layout="centered")

# Initialize chat sessions
if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = {}
if "current_chat" not in st.session_state:
    st.session_state.current_chat = "New Chat"
    st.session_state.chat_sessions["New Chat"] = [
        AIMessage(content="Hi! I'm your GPT Clone. Ask me anything.")
    ]

# Sidebar for chat titles

with st.sidebar:
    st.title("🧠 GPT Clone")

    if st.button("➕ New Chat"):
        state.current_chat = "New Chat"
        state.chat_sessions["New Chat"] = [
            AIMessage(content="Hi! I'm your GPT Clone. Ask me anything.")
        ]
        st.rerun()

    st.subheader("💬 Chat History")

    for title in list(state.chat_sessions.keys()):
        cols = st.columns([6, 1, 1])  # [Title, ✏️, 🗑️]

        # Select chat
        if cols[0].button(title, key=f"select-{title}"):
            state.current_chat = title
            st.rerun()

        # ✏️ Rename
        if cols[1].button("✏️", key=f"rename-{title}"):
            new_title = st.text_input("Rename to:", value=title, key=f"input-{uuid4()}")
            if new_title and new_title != title:
                state.chat_sessions[new_title] = state.chat_sessions.pop(title)
                if state.current_chat == title:
                    state.current_chat = new_title
                st.rerun()

        # 🗑️ Delete
        if cols[2].button("🗑️", key=f"delete-{title}"):
            del state.chat_sessions[title]
            if state.current_chat == title:
                state.current_chat = "New Chat"
                state.chat_sessions["New Chat"] = [
                    AIMessage(content="Hi! I'm your GPT Clone. Ask me anything.")
                ]
            st.rerun()


# Load current chat
chat_title = st.session_state.current_chat
messages = st.session_state.chat_sessions[chat_title]

# Display messages
for msg in messages:
    if isinstance(msg, AIMessage):
        st.chat_message("assistant").markdown(msg.content)
    else:
        st.chat_message("user").markdown(msg.content)

# User input
user_input = st.chat_input("Your message")

# Process input
if user_input:
    st.chat_message("user").markdown(user_input)
    messages.append(HumanMessage(content=user_input))

    # Rename "New Chat" to actual title (first 5 words)
    if chat_title == "New Chat":
        new_title = user_input.strip().split("\n")[0][:40]  # Limit to 40 chars
        if new_title in st.session_state.chat_sessions:
            new_title += " (1)"
        st.session_state.chat_sessions[new_title] = st.session_state.chat_sessions.pop("New Chat")
        st.session_state.current_chat = new_title
        chat_title = new_title

    # LLM setup using LangChain's unified factory. We use the OpenAI-compatible
    # endpoint (OpenRouter) but specify the model explicitly. We pass
    # model_provider="openai" so the OpenAI integration (langchain-openai)
    # is used while targeting OpenRouter via `openai_api_base`.
    chat = init_chat_model(
        model="mistralai/mistral-7b-instruct",
        model_provider="openai",
        openai_api_base="https://openrouter.ai/api/v1",
        openai_api_key=api_key,
    )

    with st.spinner("Thinking..."):
        response = chat(messages)

    st.chat_message("assistant").markdown(response.content)
    messages.append(AIMessage(content=response.content))
    

# Store uploaded content per chat
if "uploaded_files" not in state:
    state.uploaded_files = {}
if chat_title not in state.uploaded_files:
    state.uploaded_files[chat_title] = {"pdf": [], "images": []}

st.divider()
st.subheader("📎 Upload Files")

handle_pdf_upload(state, chat_title, messages)
handle_image_upload(state, chat_title, messages)


