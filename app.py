import streamlit as st
import numpy as np
import faiss
import pickle
from sentence_transformers import SentenceTransformer
import os
import random

# ------------------------------------
# Absolute Paths
# ------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FAISS_INDEX_PATH = os.path.join(BASE_DIR, "faiss_index.bin")
CHUNKS_PATH = os.path.join(BASE_DIR, "chunks.pkl")

# ------------------------------------
# Load FAISS + Chunks
# ------------------------------------
try:
    index = faiss.read_index(FAISS_INDEX_PATH)
    chunks = pickle.load(open(CHUNKS_PATH, "rb"))
except Exception as e:
    st.error("❌ FAISS vector database not found!")
    st.write("👉 Missing files:")
    st.write(FAISS_INDEX_PATH)
    st.write(CHUNKS_PATH)
    st.stop()

# ------------------------------------
# Load Embedding Model (GPU)
# ------------------------------------
model = SentenceTransformer("all-MiniLM-L6-v2", device="cuda")

# ------------------------------------
# Greeting Dictionary
# ------------------------------------
greetings = {
    ("hi", "hello", "hey", "hlo", "hola", "yo", "hey there"): [
        "Hello! 👋 How can I help you today?",
        "Hi there! 😊 What would you like to know?",
        "Hey! Ready when you are!",
        "Hello! Ask me anything."
    ],

    ("good morning",): [
        "Good Morning! ☀️ How can I assist you?",
    ],

    ("good afternoon",): [
        "Good Afternoon! 🌤️ How can I help you?"
    ],

    ("good evening",): [
        "Good Evening! 🌙 What can I do for you?"
    ],

    ("how are you", "how r u", "how are u"): [
        "I'm doing great! Thanks for asking 😊",
        "I'm functioning perfectly! How can I help you?"
    ],

    ("what's up", "wassup", "sup"): [
        "All good here! What about you? 😄",
        "Just here helping you. What's up?"
    ]
}

# ------------------------------------
# Greeting Detector (NO false triggers)
# ------------------------------------
def is_greeting(q):
    q = q.lower().strip()
    words = q.split()

    for keys, replies in greetings.items():
        for k in keys:
            k = k.lower()

            # exact full match
            if q == k:
                return random.choice(replies)

            # exact word match
            if k in words:
                return random.choice(replies)

            # starts with greeting
            if q.startswith(k + " "):
                return random.choice(replies)

            # ends with greeting
            if q.endswith(" " + k):
                return random.choice(replies)

    return None


# ------------------------------------
# Main Answer Generator (RAG + Greetings)
# ------------------------------------
def get_answer(question):

    # First check greeting/small talk
    greet_reply = is_greeting(question)
    if greet_reply:
        return greet_reply

    # FAISS retrieval
    embed = model.encode([question], convert_to_numpy=True).astype("float32")
    distances, indices = index.search(embed, 3)

    answer = "### 🔎 Top matching information:\n\n"

    for idx in indices[0]:
        if idx < len(chunks):
            answer += f"- {chunks[idx]}\n\n"

    return answer.strip()


# ------------------------------------
# Streamlit UI Setup
# ------------------------------------
st.set_page_config(page_title="KSH Chatbot", layout="centered")
st.markdown("<div class='clearfix'></div>", unsafe_allow_html=True)
st.markdown("""
<div style="
    background: linear-gradient(135deg, #2563eb, #3b82f6);
    padding: 15px;
    border-radius: 12px;
    color: white;
    text-align: center;
    font-size: 16px;
    font-weight: 500;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
    margin-bottom: 15px;
">
    🤖 <b>Smart AI Assistant</b><br>
    Ask anything from your knowledge base — I’ll find the best answer instantly ⚡
</div>
""", unsafe_allow_html=True)

st.markdown("""
<p style='text-align:center; color:#64748b; font-size:14px;'>
💡 Try: "What is AI?" | "Explain machine learning" | "Project details"
</p>
""", unsafe_allow_html=True)

st.markdown("""
<style>

/* Background */
.stApp {
    background-color: #f1f5f9;
}

/* Center content */
.block-container {
    max-width: 700px;
    margin: auto;
}

/* Header */
h1 {
    text-align: center;
    color: #2563eb;
    font-weight: 800;
}

/* User bubble */
.chat-bubble-user {
    float: right;
    background: #2563eb;
    color: black;
    padding: 10px 15px;
    border-radius: 15px 15px 0px 15px;
    margin: 10px 0;
    max-width: 75%;
}

/* Bot bubble */
.chat-bubble-bot {
    float: left;
    background: #ffffff;
    color: black;
    padding: 10px 15px;
    border-radius: 15px 15px 15px 0px;
    margin: 10px 0;
    max-width: 75%;
    border: 2px solid black;
}

/* Clear fix */
.clearfix {
    clear: both;
}

/* Input box (IMPORTANT FIX) */
input[type="text"] {
  border:1px solid black;
      background: aliceblue;
      color:black;
    padding: 5px !important;
}

/* Input focus */
input[type="text"]:focus {
   color:black;
    
}
input[type="text"]::placeholder {
    color: #2563eb;
     text-align:right;
}
[data-testid="stTextInput"] {
    position: relative;
}

[data-testid="stTextInput"]::after {
    content: "Press Enter ↵";
    position: absolute;
    right: 14px;
    top: 38px;
    color: #2563eb;
    font-size: 12px;
    pointer-events: none;
    opacity: 0.8;
}
</style>
""", unsafe_allow_html=True)
# ------------------------------------
# Chat History
# ------------------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display past messages
for chat in st.session_state.chat_history:
    st.markdown(f"<div class='chat-bubble-user'><b>You:</b><br>{chat['user']}</div>",
                unsafe_allow_html=True)
    st.markdown("<div style='clear: both;'></div>", unsafe_allow_html=True)

    st.markdown(f"<div class='chat-bubble-bot'><b>Bot:</b><br>{chat['bot']}</div>",
                unsafe_allow_html=True)
    st.markdown("<div style='clear: both;'></div>", unsafe_allow_html=True)


# ------------------------------------
# Input handler
# ------------------------------------
def handle_send():
    question = st.session_state.input_box.strip()
    if question:
        reply = get_answer(question)
        st.session_state.chat_history.append({
            "user": question,
            "bot": reply
        })
    st.session_state.input_box = ""  # Clear textbox


st.text_input("Type your message:", key="input_box" , on_change=handle_send)
st.markdown("""
<style>

/* Label text (Type your message:) */
label {
    font-size: 18px !important;
    color: #2563eb !important;
    font-weight: 600;
}

/* Input box text */
input[type="text"] {
    font-size: 16px !important;
   
}

</style>
""", unsafe_allow_html=True)
