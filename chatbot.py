import streamlit as st
import ollama

# 🔹 Page setup
st.set_page_config(page_title="JARVIS AI", layout="wide")

# 🔹 Title
st.title("🤖 JARVIS - Personal AI Assistant")

# 🔹 SYSTEM PROMPT (Jarvis personality)
SYSTEM_PROMPT = {
    "role": "system",
    "content": """
You are JARVIS, a highly intelligent personal AI assistant.

Personality:
- Speak confidently and clearly
- Keep answers concise but insightful
- Add slight wit when appropriate

Behavior:
- Help the user learn step-by-step
- Simplify complex topics
- Give structured answers when needed

Tone:
- Smart
- Professional
- Friendly but not casual
"""
}

# 🔹 Memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# 🔹 Show previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 🔹 Clear chat button
if st.button("🧹 Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# 🔹 Input box
user_input = st.chat_input("Ask me anything...")

if user_input:
    # Show user message
    st.chat_message("user").write(user_input)

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # 🔹 Limit memory (last 6 messages)
    messages = [SYSTEM_PROMPT] + st.session_state.messages[-6:]

    # 🔹 Call Ollama
    response = ollama.chat(
        model="gemma3:4b",
        messages=messages,
        options={
            "temperature": 0.5
        }
    )

    reply = response["message"]["content"]

    # 🔹 Show assistant reply
    st.chat_message("assistant").write(reply)

    # 🔹 Save assistant reply
    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })