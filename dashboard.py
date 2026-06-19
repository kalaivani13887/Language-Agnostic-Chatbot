# ============================================================
# dashboard.py
# DASHBOARD PAGE MODULE
#
# This file contains only Dashboard Page UI and logic.
# It is imported and used by app.py
# ============================================================

import streamlit as st


def logout():
    """
    Clears session and returns to login
    """

    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.full_name = None
    st.session_state.page = "login"


def show_dashboard_page():
    """
    Renders Dashboard Page
    """

    st.markdown(f"""
    <div class="welcome-card">
        <h3>👋 Welcome, {st.session_state.full_name}</h3>
        <p>Username: {st.session_state.username}</p>
    </div>
    """, unsafe_allow_html=True)

    if "chat_count" not in st.session_state:
        st.session_state.chat_count = 0

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Chats",
            st.session_state.chat_count
        )

    with col2:
        st.metric(
            "Status",
            "Active"
        )

    with col3:
        st.metric(
            "AI Mode",
            "Chatbot"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    col_a, col_b, col_c = st.columns(3)

    with col_a:

        if st.button("🤖 Open Chat"):

            st.session_state.page = "chatbot"

            st.rerun()

    with col_b:

        if st.button("📜 View History"):

            st.session_state.page = "history"

            st.rerun()

    with col_c:

        if st.button("🚪 Logout"):

            logout()

            st.rerun()
