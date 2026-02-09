# GPT Clone Chatbot 🤖

A modern, multi-chat, file-uploading chatbot UI built with [Streamlit](https://streamlit.io/) and [LangChain](https://python.langchain.com/), powered by [OpenRouter](https://openrouter.ai/) (OpenAI-compatible API).  
Supports PDF upload per chat, chat history, and a ChatGPT-like interface.

---

## Features

- **ChatGPT-style UI** with multi-chat sidebar
- **OpenRouter API** for LLM responses (free and paid models)
- **PDF upload** support per chat session
- **Chat history** with rename and delete options
- **Session persistence** using Streamlit's session state

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/maannssi/mychatbot.git
cd mychatbot
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

If you don't have a `requirements.txt`, install manually:

```bash
pip install streamlit langchain python-dotenv PyPDF2
```

### 4. Set up your API key

- Get a free API key from [OpenRouter](https://openrouter.ai/)
- Create a `.env` file in your project root:

```
OPENROUTER_API_KEY=sk-or-your-openrouter-key-here
```

**Do not share your `.env` file or commit it to GitHub!**

---

## Usage

```bash
streamlit run main.py
```

- The app will open in your browser.
- Use the sidebar to create, rename, or delete chats.
- Upload PDFs to each chat.
- Type your message and chat with the AI!

---

## File Structure

```
mychatbot/
│
├── main.py             # Main Streamlit app
├── file_uploads.py     # File upload logic
├── .env                # Your API key (not committed)
├── .gitignore
└── requirements.txt    # (optional) Python dependencies
```

---

## Customization

- Change the LLM model in `main.py` by editing the `model` parameter in `ChatOpenAI`.
- Adjust the UI or add more features as you like!

---

## License

MIT License

---

## Credits

- [Streamlit](https://streamlit.io/)
- [LangChain](https://python.langchain.com/)
- [OpenRouter](https://openrouter.ai/)
