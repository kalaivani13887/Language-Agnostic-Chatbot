# ============================================================
# registration.py
# REGISTRATION PAGE MODULE
#
# This file contains only Registration Page UI and logic.
# It is imported and used by app.py
# ============================================================

import streamlit as st
import auth


def validate_input(full_name, username, password):

    if not full_name:
        return False, "Enter Full Name"

    if not username:
        return False, "Enter Username"

    if not password:
        return False, "Enter Password"

    return True, "Valid"


def show_registration_page():
    """
    Renders Registration Page
    """

    st.markdown("""
    <div class="welcome-card">
        <h3>📝 Create Account</h3>
        <p>Register to access chatbot</p>
    </div>
    """, unsafe_allow_html=True)

    full_name = st.text_input("Full Name")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button("✅ Register"):

            valid, msg = validate_input(
                full_name,
                username,
                password
            )

            if valid:

                success = auth.register_user(
                    full_name,
                    username,
                    password
                )

                if success:

                    st.success(
                        "Registration Successful"
                    )

                    st.session_state.page = "login"

                    st.rerun()

                else:

                    st.error(
                        "Username already exists"
                    )

            else:

                st.warning(msg)

    with col2:

        if st.button("← Login"):

            st.session_state.page = "login"

            st.rerun()
