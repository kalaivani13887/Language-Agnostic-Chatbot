import streamlit as st
import json
import os
import hashlib
import requests
from langdetect import detect
import google.generativeai as genai

# =========================
# USER DB
# =========================
USER_DB = "users.json"
CHAT_DB = "chat_history.json"



# =========================
# HASH PASSWORD
# =========================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# =========================
# LOAD USERS
# =========================
def load_users():
    if not os.path.exists(USER_DB):
        with open(USER_DB, "w") as f:
            json.dump({}, f)

    try:
        with open(USER_DB, "r") as f:
            return json.load(f)
    except:
        return {}

# =========================
# SAVE USERS
# =========================
def save_users(users):
    with open(USER_DB, "w") as f:
        json.dump(users, f, indent=2)
# =========================
# CHAT HISTORY
# =========================
def load_chat_history():
    if not os.path.exists(CHAT_DB):
        with open(CHAT_DB, "w") as f:
            json.dump([], f)

    try:
        with open(CHAT_DB, "r") as f:
            return json.load(f)
    except:
        return []

def save_chat(username, user_message, bot_response):
    chats = load_chat_history()

    chats.append({
        "username": username,
        "user_message": user_message,
        "bot_response": bot_response
    })

    with open(CHAT_DB, "w") as f:
        json.dump(chats, f, indent=2)
# =========================
# REGISTER
# =========================
def register_user(full_name, username, password):
    users = load_users()

    if username in users:
        return False

    users[username] = {
        "full_name": full_name,
        "password": hash_password(password)
    }

    save_users(users)
    return True

# =========================
# LOGIN
# =========================
def login_user(username, password):
    users = load_users()

    if username not in users:
        return None

    if users[username]["password"] == hash_password(password):
        return users[username]["full_name"]

    return None

# =========================# =========================
# LANGUAGE DETECTION
# =========================
def detect_language(text):
    try:
        return detect(text)
    except:
        return "en"



genai.configure(api_key="AIza........")

model = genai.GenerativeModel("gemini-2.5-flash")



# =========================
# AI CHATBOT
# =========================
def get_ai_response(prompt):
    lang = detect_language(prompt)

    try:
        response = model.generate_content(
            f"""
You are a multilingual AI chatbot.
Reply in the SAME language as the user.

Language: {lang}
User: {prompt}
"""
        )
        return response.text

    except Exception as e:
        return f"AI Error: {e}"

# =========================
# SESSION INIT
# =========================
if "page" not in st.session_state:
    st.session_state.page = "login"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

st.set_page_config(page_title="AI Chatbot App", layout="centered")
st.title("🤖 AI Chatbot System")

# =========================
# LOGOUT
# =========================
def logout():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()


# =========================
# DASHBOARD
# =========================
def dashboard():
    st.subheader(f"👋 Welcome {st.session_state.full_name}")

    if "chat_count" not in st.session_state:
        st.session_state.chat_count = 0

    if "messages" not in st.session_state:
        st.session_state.messages = []

    st.metric("Total Chats", st.session_state.chat_count)

    # Show current chat
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.write("🧑 You:", msg["text"])
        else:
            st.write("🤖 AI:", msg["text"])

    user_input = st.text_input("Type message")

    if st.button("Send"):
        if user_input:

            st.session_state.messages.append({
                "role": "user",
                "text": user_input
            })

            reply = get_ai_response(user_input)

            save_chat(st.session_state.full_name, user_input, reply)

            st.session_state.messages.append({
                "role": "ai",
                "text": reply
            })

            st.session_state.chat_count += 1
            st.rerun()

    # View Chat History
    if st.button("📜 View Chat History"):
        chats = load_chat_history()

        if len(chats) == 0:
            st.info("No chat history found.")
        else:
            for chat in chats:
                st.write("👤", chat["username"])
                st.write("🧑 You:", chat["user_message"])
                st.write("🤖 AI:", chat["bot_response"])
                st.write("------------------------")

    # Clear Chat History
    if st.button("🗑️ Clear Chat History"):
        with open(CHAT_DB, "w") as f:
            json.dump([], f)

        st.success("Chat history cleared successfully!")

    # Logout
    if st.button("🚪 Logout"):
        logout()

    
# =========================
# LOGIN PAGE
# =========================
def login_page():
    st.subheader("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = login_user(username, password)

        if user:
            st.session_state.logged_in = True
            st.session_state.full_name = user
            st.rerun()
        else:
            st.error("Invalid credentials")

    if st.button("Create Account"):
        st.session_state.page = "register"
        st.rerun()

# =========================
# REGISTER PAGE
# =========================
def register_page():
    st.subheader("📝 Register")

    full_name = st.text_input("Full Name")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        if register_user(full_name, username, password):
            st.success("Account created successfully")
            st.session_state.page = "login"
            st.rerun()
        else:
            st.error("Username already exists")

    if st.button("Back"):
        st.session_state.page = "login"
        st.rerun()

# =========================
# ROUTING
# =========================
if not st.session_state.logged_in:
    if st.session_state.page == "login":
        login_page()
    else:
        register_page()
else:
    dashboard()
