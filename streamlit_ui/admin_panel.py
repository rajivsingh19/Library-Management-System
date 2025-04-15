import streamlit as st
import requests
from update_profile import update_profile
from book_panel import show_book_management

API_URL = "http://localhost:8000"  # 🔁 Change if needed


def show_admin_panel(token):
    st.title("🛡️ Admin Panel")

    st.sidebar.title("🧭 Navigation")
    selection = st.sidebar.radio("Go to", [
        "👤 Profile",
        "🔑 Access Management",
        "🎓 Promote Users",
        "👤 User Permissions",
        "📚 Book Management",
    ])
    if selection == "👤 Profile":
        update_profile(token)
    elif selection == "🔑 Access Management":
        show_access_management(token)
    elif selection == "🎓 Promote Users":
        show_promote_users(token)
    elif selection == "👤 User Permissions":
        show_user_permissions(token)
    elif selection == "📚 Book Management":
        show_book_management(token)


def show_access_management(token):
    st.subheader("📜 Access Control Rules")

    headers = {"token": token}

    role_options = ["admin", "librarian", "member"]
    resource_options = ["book", "user", "access", "borrowing", "user_permission"]
    action_options = ["create", "read", "update", "delete", "promote", "add", "borrow", "return"]

    try:
        response = requests.get(f"{API_URL}/users/access_list/", headers=headers)
        if response.status_code == 200:
            access_rules = response.json()
            for rule in access_rules:
                with st.expander(f"🔧 {rule['role']} → {rule['resource']} → {rule['action']}"):
                    new_role = st.selectbox("Role", role_options, index=role_options.index(rule["role"]), key=f"role_{rule['id']}")
                    new_resource = st.selectbox("Resource", resource_options, index=resource_options.index(rule["resource"]), key=f"res_{rule['id']}")
                    new_action = st.selectbox("Action", action_options, index=action_options.index(rule["action"]), key=f"act_{rule['id']}")
                    if st.button("Update", key=f"update_{rule['id']}"):
                        update_payload = {"role": new_role, "resource": new_resource, "action": new_action}
                        res = requests.put(f"{API_URL}/users/update_access/{rule['id']}", json=update_payload, headers=headers)
                        if res.status_code == 200:
                            st.success("✅ Rule updated successfully")
                            st.rerun()
                        else:
                            st.error("❌ Failed to update rule")
        else:
            st.error("❌ Failed to fetch access rules")
    except Exception as e:
        st.error(f"🚨 Error: {e}")

    st.markdown("---")
    st.subheader("➕ Add New Access Rule")

    new_role = st.selectbox("New Role", role_options, key="new_role")
    new_resource = st.selectbox("New Resource", resource_options, key="new_resource")
    new_action = st.selectbox("New Action", action_options, key="new_action")

    if st.button("Add Access Rule"):
        data = {"role": new_role, "resource": new_resource, "action": new_action}
        res = requests.post(f"{API_URL}/users/add_access/", json=data, headers=headers)
        if res.status_code == 201:
            st.success("✅ Access rule added successfully")
            st.rerun()
        else:
            st.error("❌ Failed to add access rule")


def show_promote_users(token):
    st.subheader("👥 Promote Users")

    headers = {"token": token}

    try:
        res = requests.get(f"{API_URL}/users/get_users/", headers=headers)
        if res.status_code == 200:
            users = res.json()
            user_options = {f"{u['username']} ({u['role']})": u['id'] for u in users}

            selected_user = st.selectbox("Select User to Promote", list(user_options.keys()))
            selected_user_id = user_options[selected_user]

            new_role = st.selectbox("Select New Role", ["member", "librarian", "admin"])

            if st.button("Promote"):
                promote_url = f"{API_URL}/promote/users/promote/{selected_user_id}?new_role={new_role}"
                res = requests.put(promote_url, headers=headers)
                if res.status_code == 200:
                    st.success(f"✅ {selected_user} promoted to {new_role}")
                    st.rerun()
                else:
                    st.error("❌ Promotion failed: " + res.text)
        else:
            st.error("❌ Failed to fetch users")
    except Exception as e:
        st.error(f"🚨 Error: {e}")


# def show_user_permissions(token):
#     st.subheader("👤 Manage User-Specific Permissions")

#     headers = {"token": token}

#     try:
#         # Fetch users
#         users_res = requests.get(f"{API_URL}/users/get_users/", headers=headers)
#         # if users_res.status_code != 200:
#         #     st.error("Failed to fetch users")
#         #     return
#         # users = users_res.json()
#         # user_dict = {f"{u['username']} ({u['role']})": u['id'] for u in users}
#         user_map = {}
#         if users_res.status_code == 200:
#             for user in users_res.json():
#                 user_map[user["id"]] = {
#                     "username": user["username"],
#                     "email": user["email"]
#                 }
#         # Fetch existing user permissions
#         perm_res = requests.get(f"{API_URL}/get_user_permissions/", headers=headers)
#         if perm_res.status_code == 200:
#             permissions = perm_res.json()
#             for p in permissions:
#                 with st.expander(f"🔧 {p['user_id']} → {p['resource']} → {p['action']}"):
#                     st.write("User ID:", p["user_id"])
#                     st.write("Resource:", p["resource"])
#                     st.write("Action:", p["action"])
#                     if st.button("🗑 Delete", key=f"del_{p['id']}"):
#                         del_url = f"{API_URL}/delete_user_permissions/?user_id={p['user_id']}&resource={p['resource']}&action={p['action']}"
#                         del_res = requests.delete(del_url, headers=headers)
#                         if del_res.status_code == 200:
#                             st.success("✅ Permission deleted")
#                             st.rerun()
#                         else:
#                             st.error("❌ Failed to delete")

#         st.markdown("---")
#         st.subheader("➕ Add User-Specific Permission")

#         selected_user = st.selectbox("Select User", list(user_map.keys()))
#         selected_user_id = user_map[selected_user]

#         resource = st.text_input("Resource (e.g., book, user, borrowing)")
#         action = st.text_input("Action (e.g., create, read, update, delete)")

#         if st.button("Add Permission"):
#             add_payload = {
#                 "user_id": selected_user_id,
#                 "resource": resource,
#                 "action": action
#             }
#             add_res = requests.post(f"{API_URL}/add_user_permissions/", params=add_payload, headers=headers)
#             if add_res.status_code == 200:
#                 st.success("✅ Permission added")
#                 st.rerun()
#             else:
#                 st.error(f"❌ Failed to add permission: {add_res.text}")

#     except Exception as e:
#         st.error(f"🚨 Error: {e}")
def show_user_permissions(token):
    st.subheader("👤 Manage User-Specific Permissions")

    headers = {"token": token}

    try:
        # 🔄 Fetch users and map user_id to user info
        users_res = requests.get(f"{API_URL}/users/get_users/", headers=headers)
        user_map = {}
        user_display_map = {}
        if users_res.status_code == 200:
            for user in users_res.json():
                user_map[user["id"]] = {
                    "username": user["username"],
                    "email": user["email"],
                    "role":user["role"]
                }
                display_name = f"{user['username']} ({user['email']}) - {user['role'].capitalize()}"
                user_display_map[display_name] = user["id"]
        else:
            st.error("❌ Failed to fetch users")
            return

        # 🔄 Fetch existing user permissions
        perm_res = requests.get(f"{API_URL}/get_user_permissions/", headers=headers)
        if perm_res.status_code == 200:
            permissions = perm_res.json()
            for p in permissions:
                user_info = user_map.get(p["user_id"], {"username": "Unknown", "email": "N/A"})
                with st.expander(f"🔧 {user_info['username']} ({user_info['email']}) → {p['resource']} → {p['action']}"):
                    st.write("👤 Username:", user_info["username"])
                    st.write("📧 Email:", user_info["email"])
                    st.write("🆔 User ID:", p["user_id"])
                    st.write("📘 Resource:", p["resource"])
                    st.write("⚙️ Action:", p["action"])
                    if st.button("🗑 Delete", key=f"del_{p['user_id']}_{p['resource']}_{p['action']}"):
                        del_url = f"{API_URL}/delete_user_permissions/?user_id={p['user_id']}&resource={p['resource']}&action={p['action']}"
                        del_res = requests.delete(del_url, headers=headers)
                        if del_res.status_code == 200:
                            st.success("✅ Permission deleted")
                            st.rerun()
                        else:
                            st.error("❌ Failed to delete permission")

        else:
            st.error("❌ Failed to fetch user permissions")

        st.markdown("---")
        st.subheader("➕ Add User-Specific Permission")

        selected_user_display = st.selectbox("Select User", list(user_display_map.keys()))
        selected_user_id = user_display_map[selected_user_display]

        resource = st.text_input("Resource (e.g., book, user, borrowing)")
        action = st.text_input("Action (e.g., create, read, update, delete)")

        if st.button("Add Permission"):
            add_payload = {
                "user_id": selected_user_id,
                "resource": resource,
                "action": action
            }
            add_res = requests.post(f"{API_URL}/add_user_permissions/", params=add_payload, headers=headers)
            if add_res.status_code == 200:
                st.success("✅ Permission added")
                st.rerun()
            else:
                st.error(f"❌ Failed to add permission: {add_res.text}")

    except Exception as e:
        st.error(f"🚨 Error: {e}")
