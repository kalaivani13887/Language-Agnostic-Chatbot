import streamlit as st
from auth import register_user

st.title("📝 User Registration")

username = st.text_input("Enter Username")
password = st.text_input("Enter Password", type="password")
confirm_password = st.text_input("Confirm Password", type="password")

if st.button("Register"):
    if username == "" or password == "":
        st.error("Please fill all fields.")

    elif password != confirm_password:
        st.error("Passwords do not match.")

    else:
        if register_user(username, password):
            st.success("Registration Successful!")
        else:
            st.error("Username already exists.")