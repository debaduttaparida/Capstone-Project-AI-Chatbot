# 🤖 Nova — AI-Powered Chatbot

> **LangChain + Google Gemini 1.5 Flash + Streamlit**  
> Capstone Project — AI Application Development (Option 1)  
> 💰 **100% Free** — no credit card, no paid API

---

## 📁 Project Structure

```
Final_Capstone_Project/
├── project.ipynb        ← End-to-end Jupyter implementation
├── app.py               ← Streamlit deployment app
├── requirements.txt     ← Python dependencies
├── .env.example         ← Environment template
├── README.md            ← This file
└── report.pptx          ← Project report & architecture slides
```

---

## 🚀 Quick Start (5 Minutes)

### Step 1 — Get Your FREE API Key
1. Go to **[aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)**
2. Sign in with Google → Click **"Create API Key"**
3. Copy the key (starts with `AIza...`)

> **Free tier:** 1,500 requests/day · 15 requests/min · No cost

### Step 2 — Setup Environment
```bash
# Unzip the project
unzip Final_Capstone_Project.zip
cd Final_Capstone_Project

# Create virtual environment
python -m venv venv
source venv/bin/activate          # macOS/Linux
# venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt
```

### Step 3 — Configure API Key
```bash
# Create .env file
cp .env.example .env

# Edit .env and add your key
echo "GOOGLE_API_KEY=AIzaSy..." >> .env
```

### Step 4 — Run the App
```bash
streamlit run app.py
```
Open your browser at **http://localhost:8501** 🎉

---

## 📓 Run the Jupyter Notebook

```bash
pip install jupyter
jupyter notebook project.ipynb
```

The notebook covers the full end-to-end implementation:
- Problem statement
- LLM initialization
- Prompt engineering
- Memory setup
- Chain assembly
- 7-turn test suite
- Evaluation rubric (4.86/5.0)
- Multi-persona factory

---

## 🏗️ Architecture

```
User Input
    │
    ▼
┌──────────────────────────────────────────┐
│           Streamlit Web UI               │
│         (app.py — 4 personas)            │
└──────────────────┬───────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────┐
│         ChatPromptTemplate               │
│  ┌─ SystemMessage  (persona definition)  │
│  ├─ MessagesPlaceholder ◄── Memory       │
│  └─ HumanMessage  (user input)           │
└──────────────────┬───────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────┐
│    Google Gemini Flash Latest (FREE)        │
│    via LangChain ChatGoogleGenerativeAI  │
└──────────────────┬───────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────┐
│    ConversationBufferMemory              │
│    Stores all HumanMessage + AIMessage   │
└──────────────────────────────────────────┘
                   │
                   ▼
             Response → User
```

---

## ✨ Features

| Feature | Details |
|---|---|
| 🧠 **Multi-turn Memory** | Full conversation history retained across turns |
| 🎭 **4 Personas** | General / CodeBot / TutorBot / WritingBot |
| ⚙️ **Live Config** | Adjust model, temperature, max tokens in sidebar |
| 💾 **Export Chat** | Download full conversation as .txt file |
| 🛡️ **Error Handling** | Graceful API key, rate limit, and safety filter handling |
| 💰 **Free API** | Google Gemini 1.5 Flash — 1,500 req/day, no cost |
| 🔄 **Session Reset** | Clear conversation with one click |

---

## 📊 Evaluation Results

| Test | Name | Score |
|---|---|---|
| T1 | Greeting & Introduction | 5.0/5.0 ✅ |
| T2 | Technical Explanation | 4.75/5.0 ✅ |
| T3 | Memory Retention | 5.0/5.0 ✅ |
| T4 | Multi-Turn Follow-Up | 4.75/5.0 ✅ |
| T5 | Out-of-Scope Handling | 5.0/5.0 ✅ |
| T6 | Code Generation | 4.75/5.0 ✅ |
| T7 | Persona Consistency | 5.0/5.0 ✅ |
| **Overall** | **7/7 Passed** | **4.89/5.00** |

---

## 🔧 Configuration Options

In `app.py` sidebar:
- **Model:** `gemini-flash-latest` (fast, free) or `gemini-1.5-pro` (more capable)
- **Temperature:** 0.0 (deterministic) → 1.5 (highly creative)
- **Max Tokens:** 128 → 2048 per response

---

## 🔮 Future Improvements

- **RAG Integration** — Upload PDFs, query with semantic search via FAISS
- **Streaming** — Real-time token-by-token response display
- **Voice Input** — Whisper API for speech-to-text
- **Tool Use** — Web search, weather, calculator via LangChain agents
- **Authentication** — Multi-user with per-session memory isolation
- **Docker** — Containerized deployment to GCP/AWS

---

## 🐛 Troubleshooting

| Error | Fix |
|---|---|
| `Invalid API key` | Double-check key in sidebar or .env file |
| `429 Rate Limit` | Wait 60 seconds (free tier: 15 req/min) |
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| `Safety filter blocked` | Rephrase your question |

---

## 📦 Tech Stack

| Component | Package | Version |
|---|---|---|
| LLM API | google-generativeai | 0.7.2 |
| Orchestration | langchain | 0.2.16 |
| LLM Wrapper | langchain-google-genai | 1.0.10 |
| Web UI | streamlit | 1.38.0 |
| Config | python-dotenv | 1.0.1 |

---

*Capstone Project — AI Application Development · Option 1: AI-Powered Chatbot*
