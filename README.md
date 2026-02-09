# GPT Clone Chatbot 🤖

A modern, multi-chat, file-uploading chatbot UI built with [Streamlit](https://streamlit.io/) and [LangChain](https://python.langchain.com/), powered by [OpenRouter](https://openrouter.ai/) (OpenAI-compatible API).  
Supports PDF & image upload per chat, chat history, and a ChatGPT-like interface.

---

## 🎯 Features

- **ChatGPT-style UI** with multi-chat sidebar (create, rename, delete chats)
- **LLM Integration** via LangChain's unified factory (supports 20+ providers)
- **OpenRouter API** for cost-effective LLM responses (Mistral 7B by default)
- **PDF & Image Upload** support per chat session
- **Chat History** with persistent session state
- **Message Management** with automatic conversation context handling

---

## 🛠️ Tech Stack

### **Core Technologies**

| Technology | Purpose | Why Used |
|------------|---------|----------|
| **Streamlit** | Web UI Framework | No HTML/CSS needed; Python-only, rapid prototyping |
| **LangChain** | LLM Orchestration | Unified interface for 20+ LLM providers, conversation management |
| **OpenRouter API** | LLM API Provider | Cost-effective, supports multiple models, OpenAI-compatible |
| **Mistral 7B** | Language Model | Fast, lightweight, good for chat at low cost |
| **Python 3.12** | Runtime | Modern async support, type hints |

### **Supporting Libraries**

- **langchain-core** – Core message types (AIMessage, HumanMessage)
- **langchain-openai** – OpenAI-compatible provider integration
- **python-dotenv** – Environment variable management
- **PyPDF2** – PDF text extraction
- **Pillow** – Image handling

---

## 📚 How It Works

### **Architecture Overview**

```
┌─────────────────────────────────────┐
│   Streamlit Web UI (main.py)        │
│  - Chat display                     │
│  - File uploads                     │
│  - Session state management         │
└────────────┬────────────────────────┘
             │
             ├─ calls init_chat_model()
             │
             ↓
┌─────────────────────────────────────┐
│   LangChain (langchain.chat_models) │
│  - Unified LLM interface            │
│  - Message routing                  │
│  - Provider detection               │
└────────────┬────────────────────────┘
             │
             ├─ maps to openai provider
             │
             ↓
┌─────────────────────────────────────┐
│   OpenRouter API Proxy              │
│   https://openrouter.ai/api/v1      │
│  - Cost optimization                │
│  - Model routing                    │
└────────────┬────────────────────────┘
             │
             ↓
┌─────────────────────────────────────┐
│   Mistral 7B LLM                    │
│  (or any other model you choose)    │
└─────────────────────────────────────┘
```

### **User Interaction Flow**

1. **User Types Message** → Streamlit captures input
2. **Append to History** → Message added as `HumanMessage`
3. **Initialize LLM** → LangChain creates model instance via `init_chat_model()`
4. **Send to API** → Full conversation history sent to Mistral 7B
5. **Get Response** → AI response received and appended as `AIMessage`
6. **Display in UI** → Streamlit renders response in chat bubble
7. **Persist State** → Conversation saved in `st.session_state`

### **Key Components Explained**

#### **main.py** (Core App Logic)
- Initializes Streamlit UI with `st.set_page_config()`
- Manages chat sessions using `st.session_state` (persists across reruns)
- Creates sidebar with chat list and controls
- Displays message history with `st.chat_message()`
- Handles user input via `st.chat_input()`
- Initializes LLM using `init_chat_model()` from LangChain

#### **file_uploads.py** (File Handling)
- `handle_pdf_upload()` – Uploads PDF, extracts text, appends to chat
- `handle_image_upload()` – Uploads images, displays preview, logs metadata

#### **LangChain's `init_chat_model()`**
Instead of provider-specific imports (old way):
```python
# ❌ Old (provider-specific)
from langchain_openai import ChatOpenAI
chat = ChatOpenAI(model="gpt-4")

# ✅ New (unified factory)
from langchain.chat_models import init_chat_model
chat = init_chat_model(
    model="mistralai/mistral-7b-instruct",
    model_provider="openai",
    openai_api_base="https://openrouter.ai/api/v1",
    openai_api_key=api_key,
)
```

**Benefits:**
- Single interface for all providers
- Easy model/provider switching
- Automatic API routing
- Built-in retry logic

#### **Streamlit Session State**
```python
st.session_state.chat_sessions = {
    "Chat 1": [AIMessage(...), HumanMessage(...), ...],
    "Chat 2": [AIMessage(...), ...],
}
```
- Persists data across page reruns
- Triggered by button clicks, input changes
- No database needed for session management

---

## 🚀 Changing Models

Edit the `model` and `model_provider` in `main.py` (around line 95):

### **Use GPT-4o**
```python
chat = init_chat_model(
    model="openai/gpt-4o",
    model_provider="openai",
    openai_api_key=api_key,
)
```

### **Use Claude 3.5 Sonnet**
```python
chat = init_chat_model(
    model="anthropic/claude-3-5-sonnet-20241022",
    model_provider="anthropic",
    anthropic_api_key=api_key,
)
```

### **Use Llama 2 70B via OpenRouter**
```python
chat = init_chat_model(
    model="meta-llama/llama-2-70b-chat",
    model_provider="openai",
    openai_api_base="https://openrouter.ai/api/v1",
    openai_api_key=api_key,
)
```

See all available models at: https://openrouter.ai/models

---

## 📦 Getting Started

### **1. Clone the repository**

```bash
git clone https://github.com/maannssi/mychatbot.git
cd mychatbot
```

### **2. Create and activate a virtual environment**

```bash
# Windows
python -m venv .venv
.venv\Scripts\Activate.ps1

# Mac/Linux
python -m venv .venv
source .venv/bin/activate
```

### **3. Install dependencies**

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Required packages:**
- `streamlit` – Web UI
- `langchain` – LLM orchestration  
- `langchain-core` – Message types
- `langchain-openai` – OpenAI-compatible provider
- `python-dotenv` – Load environment variables
- `PyPDF2` – PDF text extraction
- `Pillow` – Image handling
- `openai` – OpenRouter client

### **4. Set up your API key**

1. Get a free API key from [OpenRouter](https://openrouter.ai/) (includes free credits)
2. Create a `.env` file in your project root:

```env
OPENROUTER_API_KEY=sk-or-your-openrouter-key-here
```

3. **Important:** Add `.env` to `.gitignore` (never commit API keys!)

```bash
echo ".env" >> .gitignore
```

---

## 🎮 Usage

```bash
streamlit run main.py
```

The app opens at `http://localhost:8501`

**How to use:**
1. **Sidebar Controls:**
   - ➕ **New Chat** – Create a new conversation
   - Click a chat name to switch between them
   - ✏️ **Rename** – Change chat title
   - 🗑️ **Delete** – Remove chat

2. **Chat Area:**
   - Type a message at the bottom
   - AI responds with Mistral 7B (or your chosen model)
   - All messages stored in session

3. **File Uploads:**
   - Upload PDFs – text extracted and added to context
   - Upload images – preview displayed

---

## 📂 Project Structure

```
mychatbot/
│
├── main.py                    # Main Streamlit app
│   ├── UI setup
│   ├── Session state management
│   ├── Chat logic
│   └── LLM initialization (init_chat_model)
│
├── file_uploads.py            # File handling utilities
│   ├── handle_pdf_upload()
│   └── handle_image_upload()
│
├── requirements.txt           # Python dependencies
├── .env                       # API key (NOT committed)
├── .gitignore                 # Excludes .env, __pycache__, .venv
└── README.md                  # This file
```

---

## 🔧 Customization

### **Change the LLM Model**

Edit lines 95-102 in `main.py`:

```python
chat = init_chat_model(
    model="mistralai/mistral-7b-instruct",      # ← Change this
    model_provider="openai",                     # ← And/or this
    openai_api_base="https://openrouter.ai/api/v1",
    openai_api_key=api_key,
)
```

### **Adjust UI Layout**

- Change sidebar width, colors, or fonts
- Customize chat bubble styling
- Add new Streamlit components (charts, tables, etc.)

### **Add New Features**

Examples:
- **Conversation memory summarization** – Compress old messages to save tokens
- **Conversation search** – Search through all past chats
- **Export conversations** – Save as PDF or TXT
- **Custom system prompts** – Give the AI specific instructions
- **Tool calling** – Let the LLM use external tools (search, calculator, etc.)

---
<img width="1918" height="951" alt="image" src="https://github.com/user-attachments/assets/d6f219ec-6292-4842-a5c9-27998c9d03b5" />


## 🐛 Troubleshooting

**Issue:** `ModuleNotFoundError: No module named 'langchain.schema'`
- **Fix:** Uses `langchain_core.messages` (updated in recent versions)

**Issue:** `ImportError: cannot import name 'ChatOpenAI'`
- **Fix:** Use `init_chat_model()` from `langchain.chat_models` instead

**Issue:** API calls failing with 401 Unauthorized
- **Fix:** Check your `OPENROUTER_API_KEY` in `.env` file

**Issue:** Streamlit not finding the app
- **Fix:** Make sure you're in the project folder and run `streamlit run main.py`

---

## 📊 Model Comparison

| Model | Provider | Speed | Quality | Cost | Best For |
|-------|----------|-------|---------|------|----------|
| Mistral 7B | OpenRouter | ⚡ Fast | 🟡 Good | 💰 Cheap | **Current setup** |
| GPT-4o | OpenAI | 🐌 Slow | 🟢 Excellent | 💰💰💰 Expensive | Complex tasks |
| Claude 3.5 | Anthropic | 🚗 Medium | 🟢 Excellent | 💰💰 Medium | Writing, analysis |
| Llama 2 70B | OpenRouter | 🐌 Slow | 🟡 Good | 💰 Cheap | Open-source alternative |
| Gemini 2.5 | Google | ⚡ Fast | 🟢 Excellent | 💰💰 Medium | Balanced, multimodal |

---

## 📚 Learning Resources

- **Streamlit Docs:** https://docs.streamlit.io/
- **LangChain Docs:** https://python.langchain.com/
- **OpenRouter Models:** https://openrouter.ai/models
- **LangChain Chat Models:** https://python.langchain.com/docs/integrations/chat/

---

## 📄 License

MIT License – Feel free to use and modify!

---

## 🙏 Credits

- **[Streamlit](https://streamlit.io/)** – Web UI framework
- **[LangChain](https://python.langchain.com/)** – LLM orchestration
- **[OpenRouter](https://openrouter.ai/)** – LLM API provider
- **[Mistral AI](https://mistral.ai/)** – Open-source LLM
