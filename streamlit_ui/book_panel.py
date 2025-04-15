import streamlit as st
import requests

API_URL = "http://localhost:8000"

def show_book_management(token):
    st.subheader("📚 Book Management")

    headers = {"token": token}

    # 🔄 Fetch all books
    try:
        response = requests.get(f"{API_URL}/books/books_list/", headers=headers)
        if response.status_code == 200:
            books = response.json()
            for book in books:
                with st.expander(f"📖 {book['title']} by {book['author']}"):
                    st.write("ISBN:", book["isbn"])
                    st.write("Available:", "✅ Yes" if book["is_available"] else "❌ No")

                    new_title = st.text_input("Edit Title", book["title"], key=f"title_{book['id']}")
                    new_author = st.text_input("Edit Author", book["author"], key=f"author_{book['id']}")
                    new_isbn = st.text_input("Edit ISBN", book["isbn"], key=f"isbn_{book['id']}")

                    if st.button("Update", key=f"update_{book['id']}"):
                        payload = {
                            "title": new_title,
                            "author": new_author,
                            "isbn": new_isbn
                        }
                        res = requests.put(f"{API_URL}/books/update_book/{book['id']}", json=payload, headers=headers)
                        if res.status_code == 200:
                            st.success("✅ Book updated")
                            st.rerun()
                        else:
                            st.error(f"❌ Failed to update: {res.text}")

                    if st.button("Delete", key=f"delete_{book['id']}"):
                        res = requests.delete(f"{API_URL}/books/delete_books/{book['id']}", headers=headers)
                        if res.status_code == 200:
                            st.success("🗑️ Book deleted")
                            st.rerun()
                        else:
                            st.error(f"❌ Delete failed: {res.text}")
        else:
            st.error(f"❌ Failed to fetch books: {response.text}")
    except Exception as e:
        st.error(f"🚨 Error: {e}")

    st.markdown("---")
    st.subheader("➕ Add New Book")

    title = st.text_input("Title")
    author = st.text_input("Author")
    isbn = st.text_input("ISBN")

    if st.button("Add Book"):
        payload = {
            "title": title,
            "author": author,
            "isbn": isbn
        }
        res = requests.post(f"{API_URL}/books/add_book/", json=payload, headers=headers)
        if res.status_code == 201:
            st.success("✅ Book added")
            st.rerun()
        else:
            st.error(f"❌ Failed to add book: {res.text}")
