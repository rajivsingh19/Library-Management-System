import streamlit as st
from login import login
from signup import signup
from member_panel import show_member_panel
from admin_panel import show_admin_panel
from librarian_panel import show_librarian_panel
# from librarian_panel import show_librarian_panel

# ✅ Set page config
st.set_page_config(
    page_title="📚 Library Management System",
    page_icon="📖",
    layout="centered"
)

# ✅ Step 1: Restore token and role from query params if available
params = st.query_params
if "token" in params and "role" in params:
    st.session_state.token = params["token"]
    st.session_state.role = params["role"]
if "active_page" in params:
    st.session_state.active_page = params["active_page"]

# ✅ Step 2: Initialize session state if not already
if "token" not in st.session_state:
    st.session_state.token = None
if "role" not in st.session_state:
    st.session_state.role = None
if "active_page" not in st.session_state:
    st.session_state.active_page = "My Panel"  # default page for member


# ✅ Step 3: Auth-based Navigation
if not st.session_state.token:
    menu = st.sidebar.selectbox("Navigate", ["Login", "Signup"])
    if menu == "Login":
        login()
    elif menu == "Signup":
        signup()
else:
    st.sidebar.markdown(f"**🔐 Logged in as:** `{st.session_state.role}`")

    if st.sidebar.button("🚪 Logout"):
        st.session_state.clear()
        st.query_params = {}
        st.rerun()

    # 🎯 Role-based Panel with persistent navigation
    # if st.session_state.role == "member":
    #     pages = ["My Panel", "View Books"]
    #     member_menu = st.sidebar.radio(
    #         "📋 Member Menu",
    #         pages,
    #         index=pages.index(st.session_state.active_page)
    #       )
    #     # Set selected page into session state
    #     if st.session_state.active_page != member_menu:
    #        st.session_state.active_page = member_menu
    #        st.query_params["active_page"] = member_menu
    #        st.rerun() 

    #     # Render the selected page
    #     if st.session_state.active_page == "My Panel":
    #         show_member_panel(st.session_state.token)
    #     elif st.session_state.active_page == "View Books":
    #         view_books(st.session_state.token)
    if st.session_state.role == "member":
      show_member_panel(st.session_state.token)
    elif st.session_state.role == "librarian":
        show_librarian_panel(st.session_state.token)
    elif st.session_state.role == "admin":
       show_admin_panel(st.session_state.token)
    else:
        st.error("❌ Unknown role. Contact administrator.")

