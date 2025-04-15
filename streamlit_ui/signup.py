import streamlit as st
import requests

def signup():
    st.subheader("📝 Sign Up")

    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Sign Up"):
        data = {
            "username": username,
            "email": email,
            "password": password
        }
        res = requests.post("http://localhost:8000/users/signup", json=data)
        if res.status_code == 201:
            st.success("Account created! Please login.")
        else:
            st.error(res.json().get("detail", "Something went wrong"))
