"""
AI-Powered Chatbot — Nova
Built with LangChain + Google Gemini 1.5 Flash (FREE API)

Run: streamlit run app.py
Get free API key: https://aistudio.google.com/app/apikey
"""

import os
import time
import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

# ─── Load environment ──────────────────────────────────────────────────────────
load_dotenv()

# ─── Page configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Nova — AI Chatbot",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://aistudio.google.com/app/apikey",
        "About": "Nova — AI Chatbot powered by LangChain + Google Gemini (Free)"
    }
)

# ─── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Main layout */
    .main .block-container { max-width: 780px; padding-top: 1rem; }

    /* Chat bubbles */
    .stChatMessage { border-radius: 12px; margin-bottom: 6px; }

    /* Sidebar styling */
    .css-1d391kg { background-color: #0f172a; }

    /* Input area */
    .stChatInput { border-top: 1px solid #e2e8f0; padding-top: 0.5rem; }

    /* Hide Streamlit branding */
    #MainMenu, footer { visibility: hidden; }

    /* Stats badges */
    .stat-badge {
        display: inline-block;
        background: #1e293b;
        color: #94a3b8;
        border-radius: 6px;
        padding: 2px 8px;
        font-size: 11px;
        margin: 2px;
    }

    /* Welcome card */
    .welcome-card {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 100%);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        border: 1px solid #334155;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ─── Personas ──────────────────────────────────────────────────────────────────
PERSONAS = {
    "🌟 Nova (General Assistant)": {
        "system": """You are Nova, a smart, friendly, and highly capable AI assistant.
You help users with questions, explanations, analysis, coding, and general tasks.
Be warm, concise, and professional. Remember conversation context throughout.
If you don't know something, say so honestly without fabricating facts.""",
        "greeting": "Hi! I'm **Nova**, your AI assistant. I can help with questions, explanations, code, and more. What would you like to explore today?"
    },
    "💻 CodeBot (Programming)": {
        "system": """You are CodeBot, an expert programming assistant.
You specialize in Python, JavaScript, and general software engineering.
Always provide clean, well-commented code. Explain your solutions step by step.
For bugs: identify root cause first, then provide the fix.""",
        "greeting": "Hey! I'm **CodeBot** — your programming companion. Share your code, describe a bug, or ask about any programming concept. Let's build something great!"
    },
    "📚 TutorBot (Education)": {
        "system": """You are TutorBot, a patient and encouraging educational assistant.
You explain complex topics simply using analogies and examples.
Break down difficult concepts step by step. Check understanding before moving on.
Adapt your teaching style to the student's level based on how they communicate.""",
        "greeting": "Hello! I'm **TutorBot** — I make learning fun and clear. What subject or concept would you like to master today? No question is too basic!"
    },
    "✍️ WritingBot (Content)": {
        "system": """You are WritingBot, a creative writing and content specialist.
You help with essays, stories, emails, reports, and all forms of written content.
Offer style suggestions, improve clarity, and adapt to the user's desired tone.
When editing: explain why you made each change.""",
        "greeting": "Welcome! I'm **WritingBot** — your writing partner. Share what you're working on: a story, email, essay, or anything else. Let's make it shine!"
    }
}

# ─── Session state initialization ─────────────────────────────────────────────
def init_state():
    defaults = {
        "messages": [],
        "memory": None,
        "chain": None,
        "chain_key": "",
        "total_tokens": 0,
        "turn_count": 0,
        "start_time": time.time()
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ─── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🤖 Nova Chatbot")
    st.markdown("*Powered by Google Gemini (Free)*")
    st.divider()

    # API Key
    st.markdown("### 🔑 API Key")
    #api_key = st.text_input(
    #    "Google Gemini API Key",
    #    value=os.getenv("GOOGLE_API_KEY", ""),
    #    type="password",
    #   placeholder="AIzaSy...",
    #    help="Get your FREE key at aistudio.google.com/app/apikey"
    #)
    #api_key = "AIzaSyArhTCozkdoJD2KfNZZOtN_aQeWsONCpco"
    #api_key = "AQ.Ab8RN6KJltcDUxmP-frs09pB_T_z8Xr2xUGsDLSWGD9r7iaZig"
    api_key = st.secrets["MY_API_KEY"]
    if not api_key:
        st.info("👆 Add your API key to start chatting")
        st.markdown("[**Get Free API Key →**](https://aistudio.google.com/app/apikey)")

    st.divider()

    # Persona selector
    st.markdown("### 🎭 Persona")
    persona_choice = st.selectbox(
        "Choose a chatbot persona",
        list(PERSONAS.keys()),
        index=0,
        help="Each persona has a different specialization and personality"
    )

    st.divider()

    # Model settings
    st.markdown("### ⚙️ Model Settings")
    model_choice = st.selectbox(
        "Gemini Model",
        ["gemini-flash-latest", "gemini-1.5-pro", "gemini-pro"],
        index=0,
        help="Flash = fast & free | Pro = more capable"
    )

    temperature = st.slider(
        "Temperature",
        min_value=0.0, max_value=1.5, value=0.7, step=0.05,
        help="Lower = precise | Higher = creative"
    )

    max_tokens = st.slider(
        "Max Response Length",
        min_value=128, max_value=2048, value=1024, step=128,
        help="Maximum tokens per response"
    )

    st.divider()

    # Stats
    st.markdown("### 📊 Session Stats")
    col1, col2 = st.columns(2)
    col1.metric("Turns", st.session_state.turn_count)
    session_mins = (time.time() - st.session_state.start_time) / 60
    col2.metric("Minutes", f"{session_mins:.0f}")
    st.caption(f"Messages in memory: {len(st.session_state.messages)}")
    st.caption("💰 Cost: $0.00 (Free Tier)")

    st.divider()

    # Controls
    if st.button("🗑️ Clear Conversation", use_container_width=True, type="secondary"):
        st.session_state.messages = []
        st.session_state.memory = None
        st.session_state.chain = None
        st.session_state.chain_key = ""
        st.session_state.turn_count = 0
        st.session_state.start_time = time.time()
        st.rerun()

    st.caption("---")
    st.caption("**Stack:** LangChain + Gemini + Streamlit")
    st.caption("**Capstone Project** — AI App Dev")

# ─── Build / Rebuild Chain ─────────────────────────────────────────────────────
def get_chain(api_key: str):
    """Build or retrieve the conversation chain, rebuilding if settings changed."""
    chain_key = f"{model_choice}|{temperature}|{max_tokens}|{persona_choice}|{api_key[:8] if api_key else ''}"

    if st.session_state.chain is None or st.session_state.chain_key != chain_key:
        # Keep memory if only model settings changed
        if st.session_state.memory is None:
            st.session_state.memory = ConversationBufferMemory(
                return_messages=True,
                memory_key="history",
                human_prefix="User",
                ai_prefix="Nova"
            )

        llm = ChatGoogleGenerativeAI(
            model=model_choice,
            google_api_key=api_key,
            temperature=temperature,
            max_output_tokens=max_tokens,
            convert_system_message_to_human=True
        )

        system_prompt = PERSONAS[persona_choice]["system"]
        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(system_prompt),
            MessagesPlaceholder(variable_name="history"),
            HumanMessagePromptTemplate.from_template("{input}")
        ])

        st.session_state.chain = ConversationChain(
            llm=llm,
            prompt=prompt,
            memory=st.session_state.memory,
            verbose=False
        )
        st.session_state.chain_key = chain_key

    return st.session_state.chain

# ─── Guard: API key required ───────────────────────────────────────────────────
if not api_key:
    st.markdown("""
    <div class="welcome-card">
        <h1>🤖 Nova AI Chatbot</h1>
        <p style="color:#94a3b8; margin: 12px 0;">Powered by LangChain + Google Gemini (100% Free)</p>
        <hr style="border-color:#334155; margin: 16px 0;">
        <p style="color:#e2e8f0;">To get started:</p>
        <ol style="text-align:left; color:#94a3b8; margin: 8px auto; max-width: 300px;">
            <li>Visit <strong>aistudio.google.com/app/apikey</strong></li>
            <li>Sign in with your Google account</li>
            <li>Click <strong>Create API Key</strong></li>
            <li>Paste the key in the sidebar ←</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

    st.info("👈 Enter your Google Gemini API key in the sidebar to begin")
    st.link_button("🔑 Get Free API Key", "https://aistudio.google.com/app/apikey", use_container_width=True)
    st.stop()

# ─── Main chat interface ───────────────────────────────────────────────────────
# Header
icon = persona_choice.split()[0]
bot_name = persona_choice.split("(")[0].strip().replace(icon, "").strip()
st.title(f"{icon} {bot_name}")
st.caption(f"Model: `{model_choice}` · Temp: `{temperature}` · {st.session_state.turn_count} turns · 💰 Free")

# Render chat history
for msg in st.session_state.messages:
    avatar = "👤" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# Welcome message on fresh start
if not st.session_state.messages:
    greeting = PERSONAS[persona_choice]["greeting"]
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(greeting)

# ─── Chat input & processing ───────────────────────────────────────────────────
if user_input := st.chat_input(f"Message {bot_name}..."):

    # Show user message
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Generate response
    with st.chat_message("assistant", avatar="🤖"):
        placeholder = st.empty()
        placeholder.markdown("⏳ *Thinking...*")

        try:
            chain = get_chain(api_key)
            start_t = time.time()
            response = chain.predict(input=user_input)
            elapsed = time.time() - start_t

            placeholder.markdown(response)

            # Track stats
            st.session_state.turn_count += 1
            st.session_state.messages.append({"role": "assistant", "content": response})

            # Show latency (subtle)
            st.caption(f"⏱️ {elapsed:.1f}s · Turn {st.session_state.turn_count}")

        except Exception as e:
            err = str(e)
            if "api_key" in err.lower() or "api key" in err.lower() or "invalid" in err.lower():
                placeholder.error("❌ Invalid API key. Please check your key in the sidebar.")
            elif "quota" in err.lower() or "rate" in err.lower() or "429" in err:
                placeholder.warning("⏳ Rate limit hit (free tier: 15 req/min). Please wait and try again.")
            elif "safety" in err.lower() or "block" in err.lower():
                placeholder.info("🛡️ This message was flagged by safety filters. Please rephrase your question.")
            else:
                placeholder.error(f"❌ Error: {err[:200]}")

# ─── Export chat (bottom of page) ─────────────────────────────────────────────
if st.session_state.messages and len(st.session_state.messages) >= 2:
    with st.expander("💾 Export Conversation"):
        export_text = f"# Nova Chat Export\n**Date:** {time.strftime('%Y-%m-%d %H:%M')}\n**Persona:** {persona_choice}\n\n---\n\n"
        for msg in st.session_state.messages:
            role_label = "**User**" if msg["role"] == "user" else "**Nova**"
            export_text += f"{role_label}: {msg['content']}\n\n"

        st.download_button(
            label="📥 Download as .txt",
            data=export_text,
            file_name=f"nova_chat_{time.strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain",
            use_container_width=True
        )
        st.code(export_text[:500] + ("..." if len(export_text) > 500 else ""), language=None)
