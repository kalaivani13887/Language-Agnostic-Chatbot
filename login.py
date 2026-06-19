# ============================================================
# login.py
# LOGIN PAGE MODULE
#
# This file contains only Login Page UI and logic.
# It is imported and used by app.py
# ============================================================

import streamlit as st
import auth


def validate_login(username, password):

    if not username:
        return False, "Enter Username"

    if not password:
        return False, "Enter Password"

    return True, "Valid"


def show_login_page():
    """
    Renders Login Page
    """

    st.markdown("""
    <div class="welcome-card">
        <h3>🔐 Login</h3>
        <p>Login to access chatbot</p>
    </div>
    """, unsafe_allow_html=True)

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button("Login"):

            valid, msg = validate_login(
                username,
                password
            )

            if valid:

                user = auth.login_user(
                    username,
                    password
                )

                if user:

                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.full_name = user

                    st.session_state.page = "dashboard"

                    st.rerun()

                else:

                    st.error(
                        "Invalid Username or Password"
                    )

            else:

                st.warning(msg)

    with col2:

        if st.button("Create Account"):

            st.session_state.page = "register"

            st.rerun()
