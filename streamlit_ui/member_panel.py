import streamlit as st
import requests
from update_profile import update_profile
API_URL = "http://localhost:8000"  # Update if your backend runs elsewhere

def show_member_panel(token):
    st.title("🛡️ Member Panel")

    st.sidebar.title("🧭 Navigation")
    selection = st.sidebar.radio("Go to", [
        "👤 Profile",
        "🟢 Borrow Books",
        "🔁 Return Books"
    ])

    if selection == "👤 Profile":
        update_profile(token)
    elif selection == "🟢 Borrow Books":
        show_borrow_books(token)
    elif selection == "🔁 Return Books":
        show_return_books(token)

def show_borrow_books(token):
    st.subheader("📖 Available Books to Borrow")
    headers = {"token": token}

    try:
        res = requests.get(f"{API_URL}/books/books_list/", headers=headers)
        if res.status_code == 200:
            books = res.json()
            available_books = [b for b in books if b["is_available"]]

            if not available_books:
                st.info("No books available to borrow at the moment.")
                return

            book_map = {f"{b['title']} by {b['author']}": b['id'] for b in available_books}
            selected = st.selectbox("Select a book to borrow", list(book_map.keys()))

            if st.button("📚 Borrow Book"):
                book_id = book_map[selected]
                borrow_url = f"{API_URL}/borrowings/borrow_book/{book_id}"
                res = requests.post(borrow_url, headers=headers)

                if res.status_code == 200:
                    st.success(res.json()["message"])
                    st.rerun()
                else:
                    st.error(f"Failed: {res.text}")
        else:
            st.error("❌ Failed to fetch books")
    except Exception as e:
        st.error(f"🚨 Error: {e}")

def show_return_books(token):
    st.subheader("🔁 Return Borrowed Books")
    headers = {"token": token}

    try:
        res = requests.get(f"{API_URL}/profile/get_borrowed_books", headers=headers)
        if res.status_code == 200:
            user_data = res.json()
            borrowed_books = [b for b in user_data["borrowed_books"] if b["returned_at"] is None]

            if not borrowed_books:
                st.info("You have no borrowed books to return.")
                return

            book_map = {
                 f"{b['title']} (Borrowed on {b['borrowed_at']})": b['book_id'] for b in borrowed_books
                        }
            selected = st.selectbox("Select a book to request return", list(book_map.keys()))

            if st.button("📤 Request Return"):
                book_id = book_map[selected]
                return_url = f"{API_URL}/borrowings/return_book/{book_id}"  # Change this if backend uses book_id instead
                res = requests.post(return_url, headers=headers)

                if res.status_code == 200:
                    st.success(res.json()["message"])
                    st.rerun()
                else:
                    st.error(f"Failed: {res.text}")
        else:
            st.error("❌ Failed to fetch borrowed books")
    except Exception as e:
        st.error(f"🚨 Error: {e}")
