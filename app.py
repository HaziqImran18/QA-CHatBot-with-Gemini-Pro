import streamlit as st
from dotenv import load_dotenv
import os
import shelve
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize the Gemini Pro model and chat
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

# Function to get response from Gemini
def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    full_response = ""
    # Ensure response is handled correctly
    for chunk in response:
        # Adjust according to actual attributes or methods available in the response
        if hasattr(chunk, 'text'):
            full_response += chunk.text
        else:
            full_response += str(chunk)  # Fallback to string representation if needed
    return full_response

st.title("Gemini-Pro Chatbot")

USER_AVATAR = "👤"
BOT_AVATAR = "🤖"

# Ensure gemini_model is initialized in session state
if "gemini_model" not in st.session_state:
    st.session_state["gemini_model"] = "gemini-pro"

# Load chat history from shelve file
def load_chat_history():
    with shelve.open("chat_history") as db:
        return db.get("messages", [])

# Save chat history to shelve file
def save_chat_history(messages):
    with shelve.open("chat_history") as db:
        db["messages"] = messages

# Initialize or load chat history
if "messages" not in st.session_state:
    st.session_state.messages = load_chat_history()

# Sidebar with a button to delete chat history
with st.sidebar:
    if st.button("Delete Chat History"):
        st.session_state.messages = []
        save_chat_history([])

# Display chat messages
for message in st.session_state.messages:
    avatar = USER_AVATAR if message["role"] == "user" else BOT_AVATAR
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Main chat interface
if prompt := st.chat_input("How can I help?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(prompt)

    # Get response from Gemini
    full_response = get_gemini_response(prompt)

    with st.chat_message("assistant", avatar=BOT_AVATAR):
        st.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Save chat history after each interaction
save_chat_history(st.session_state.messages)
