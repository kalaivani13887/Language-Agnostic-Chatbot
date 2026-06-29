import streamlit as st
import json
import os
import hashlib

# =========================
# USER DATABASE FILE
# =========================
USER_DB = "users.json"

# =========================
# PASSWORD HASH
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

    with open(USER_DB, "r") as f:
        return json.load(f)

# =========================
# SAVE USERS
# =========================
def save_users(users):
    with open(USER_DB, "w") as f:
        json.dump(users, f, indent=2)

# =========================
# REGISTER USER
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
# LOGIN USER
# =========================
def login_user(username, password):
    users = load_users()

    if username not in users:
        return None

    if users[username]["password"] == hash_password(password):
        return users[username]["full_name"]

    return None

# =========================
# INIT SESSION STATE
# =========================
if "page" not in st.session_state:
    st.session_state.page = "login"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# =========================
# PAGE UI
# =========================
st.set_page_config(page_title="AI Chatbot App", layout="centered")

st.title("🤖 AI Chatbot System")

# =========================
# LOGOUT FUNCTION
# =========================
def logout():
    st.session_state.logged_in = False
    st.session_state.page = "login"
    st.session_state.username = None
    st.session_state.full_name = None

# =========================
# DASHBOARD
# =========================
def dashboard():
    st.subheader(f"👋 Welcome {st.session_state.full_name}")

    if "chat_count" not in st.session_state:
        st.session_state.chat_count = 0

    st.metric("Total Chats", st.session_state.chat_count)

    if st.button("➕ Increase Chat Count"):
        st.session_state.chat_count += 1
        st.rerun()

    if st.button("🚪 Logout"):
        logout()
        st.rerun()

# =========================
# LOGIN PAGE
# =========================
def login_page():
    st.subheader("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if not username or not password:
            st.warning("Fill all fields")
        else:
            user = login_user(username, password)

            if user:
                st.session_state.logged_in = True
                st.session_state.username = username
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
        if not full_name or not username or not password:
            st.warning("Fill all fields")
        else:
            success = register_user(full_name, username, password)

            if success:
                st.success("Account created successfully")
                st.session_state.page = "login"
                st.rerun()
            else:
                st.error("Username already exists")

    if st.button("Back to Login"):
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
