import streamlit as st
import requests
from update_profile import update_profile
from book_panel import show_book_management

API_URL = "http://localhost:8000"  # Update if needed


def show_librarian_panel(token):
    st.title("🛡️ Librarian Panel")

    st.sidebar.title("🧭 Navigation")
    selection = st.sidebar.radio("Go to", [
        "👤 Profile",
        "📚 Borrowing Tracker",
        "🔄 Manage Borrowings",
        "📘 Manage Books",
    ])

    if selection == "👤 Profile":
        update_profile(token)
    elif selection == "📚 Borrowing Tracker":
        show_borrowing_tracker(token)
    elif selection == "🔄 Manage Borrowings":
        manage_borrowings(token)
    elif selection == "📘 Manage Books":
        show_book_management(token)


def show_borrowing_tracker(token):
    st.subheader("📚 Borrowing Tracker")

    headers = {"token": token}

    try:
        res = requests.get(f"{API_URL}/borrowings/all_borrowed_books/", headers=headers)
        if res.status_code == 200:
            borrowed_books = res.json()["borrowed_books"]
            if not borrowed_books:
                st.info("No books have been borrowed yet.")
                return
            for book in borrowed_books:
                st.write(f"**Title**: {book['book_title']}")
                st.write(f"**Borrowed by**: {book['borrowed_by']}")
                st.write(f"**Borrowed on**: {book['borrowed_at']}")
                st.write(f"**Due date**: {book['returned_at'] if book['returned_at'] else 'Not yet returned'}")
                st.write("---")
        else:
            st.error("❌ Failed to fetch borrowed books.")
    except Exception as e:
        st.error(f"🚨 Error: {e}")


# def manage_borrowings(token):
#     st.subheader("🔄 Manage Borrowings")

#     headers = {"token": token}

#     try:
#         res = requests.get(f"{API_URL}/borrowings/all_borrowed_books/", headers=headers)
#         if res.status_code == 200:
#             borrowed_books = res.json()["borrowed_books"]
#             # st.write(borrowed_books)

#             if not borrowed_books:
#                 st.info("No books have been borrowed yet.")
#                 return

#             book_map = {
#                 f"{b['book_title']} (Borrowed by {b['borrowed_by']})": b['book_id']
#                 for b in borrowed_books
#             }

#             selected = st.selectbox("Select a borrowed book to manage", list(book_map.keys()))

#             if st.button("🔄 Mark as Returned"):
#                 book_id = book_map[selected]
#                 return_url = f"{API_URL}/borrowings/return_book/{book_id}"
#                 res = requests.post(return_url, headers=headers)

#                 if res.status_code == 200:
#                     st.success(res.json()["message"])
#                     st.rerun()
#                 else:
#                     st.error(f"Failed: {res.text}")

#         else:
#             st.error("❌ Failed to fetch borrowed books.")
#     except Exception as e:
#         st.error(f"🚨 Error: {e}")

def manage_borrowings(token):
    st.subheader("🔄 Manage Borrowings (Return Requests)")

    headers = {"token": token}

    try:
        res = requests.get(f"{API_URL}/borrowings/all_borrowed_books/", headers=headers)
        if res.status_code == 200:
            borrowed_books = res.json()["borrowed_books"]

            # Filter only return requests that are pending
            pending_returns = [b for b in borrowed_books if b["return_requested"] and not b["returned_at"]]

            if not pending_returns:
                st.info("No pending return requests.")
                return

            book_map = {
                f"{b['book_title']} (Requested by {b['borrowed_by']})": b
                for b in pending_returns
            }

            selected = st.selectbox("Select a return request to approve", list(book_map.keys()))

            if selected:
                book_info = book_map[selected]
                st.write(f"**Book Title:** {book_info['book_title']}")
                st.write(f"**Borrowed By:** {book_info['borrowed_by']}")
                st.write(f"**Borrowed On:** {book_info['borrowed_at']}")
                st.write(f"**Return Requested:** ✅")

                if st.button("✅ Approve Return"):
                    borrowing_id = book_info["borrowing_id"]  # 👈 Change this to real borrowing_id if available
                    approve_url = f"{API_URL}/borrowings/approve_return/{borrowing_id}"
                    res = requests.post(approve_url, headers=headers)

                    if res.status_code == 200:
                        st.success(res.json()["message"])
                        st.rerun()
                    else:
                        st.error(f"❌ Failed: {res.text}")
        else:
            st.error("❌ Failed to fetch borrowed books.")
    except Exception as e:
        st.error(f"🚨 Error: {e}")
