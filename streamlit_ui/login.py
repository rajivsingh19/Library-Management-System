import streamlit as st
import requests


API_URL = "http://localhost:8000"  # Change this if your FastAPI runs on another port or server

def login():
    st.title("🔐 Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    login_btn = st.button("Login")

    if login_btn:
        if not email or not password:
            st.warning("Please fill all fields")
            return
        
        response = requests.post(f"{API_URL}/users/login", json={
            "email": email,
            "password": password
        })
        if response.status_code == 200:
            data = response.json()
            st.success(f"Welcome back! Role: {data['role']}")

    # Save in session
            st.session_state.token = data["access_token"]
            st.session_state.role = data["role"]

    # Save in query params
            st.query_params.update(token=data["access_token"], role=data["role"])
            st.write("Role from response:", data["role"])
            st.rerun()

        else:
            st.error("Login failed. Check credentials.")

