import streamlit as st
import requests

API_URL = "http://localhost:8000"  # Update if your backend runs elsewhere

def update_profile(token):

    headers = {"token": token}
   

    # Fetch user profile data
    try:
        response = requests.get(f"{API_URL}/profile/get_my_profile", headers=headers)
        if response.status_code == 200:
            data = response.json()
            st.subheader("Current Profile Info")
            st.write(f"**Username:** {data['username']}")
            st.write(f"**Email:** {data['email']}")
            st.write(f"**Role:** {data['role']}")
            
            st.title("Update Your Profile")

            # Form to update profile
            new_username = st.text_input("New Username", value=data['username'])
            new_email = st.text_input("New Email", value=data['email'])

            if st.button("Update Profile"):
                # Send the update request to the backend
                update_data = {
                    "username": new_username,
                    "email": new_email
                }
                res = requests.put(f"{API_URL}/profile/update_profile", json=update_data, headers=headers)

                if res.status_code == 200:
                    st.success(res.json()["message"])
                    st.rerun()  # Refresh the page after successful update
                else:
                    st.error(f"Failed to update profile: {res.text}")
        else:
            st.error("Failed to fetch profile data")
    except Exception as e:
        st.error(f"Error fetching profile: {e}")


    # ------- Password Update Section -------
    st.subheader("Change Password")

    with st.form("password_form"):
        old_password = st.text_input("Old Password", type="password")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm New Password", type="password")
        submit_password = st.form_submit_button("Update Password")

    if submit_password:
        if new_password != confirm_password:
            st.error("New passwords do not match.")
        else:
            payload = {
                "old_password": old_password,
                "new_password": new_password
            }

            try:
                res = requests.put(
                    f"{API_URL}/profile/password",
                    params=payload,  # Using params because your route expects query parameters
                    headers=headers
                )

                if res.status_code == 200:
                    st.success(res.json()["message"])
                else:
                    st.error(f"Failed to update password: {res.json().get('detail', res.text)}")
            except Exception as e:
                st.error(f"Error updating password: {e}")
