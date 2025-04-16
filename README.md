
# 📚 Library Book Management System

A secure and role-based E-Library Management System built with **FastAPI**, **Streamlit**, and **PostgreSQL**. It supports dynamic **RBAC**, real-time **book tracking**, and user-specific **borrowing workflows** for admins, librarians, and members.

---

## 🚀 Features

### 🔐 Authentication & Authorization
- JWT-based authentication
- RSA encryption for password handling
- Role-Based Access Control (RBAC)
- User-specific permission overrides

### 👤 User Roles
- **Admin**: Full control over users, books, access rules
- **Librarian**: Manage books and borrowing
- **Member**: Browse, borrow, and return books

### 📚 Book Management
- Add, update, delete books
- View availability in real-time
- Filter by title, author, or ISBN

### 🔁 Borrowing System
- Borrow & return books (with approval flow)
- Track borrowing history
- Prevent double borrowing of the same book

### 🧠 RBAC Controls
- Dynamic Access Control via `access_control` table
- Admin can promote users and assign user-specific rules

### 📊 Dashboard (Planned)
- Insights on popular books, categories, borrowing trends

---

## 🧱 Tech Stack

| Layer        | Technology             |
|-------------|-------------------------|
| **Backend** | FastAPI, SQLAlchemy     |
| **Frontend**| Streamlit               |
| **Database**| PostgreSQL              |
| **Auth**    | JWT, RSA encryption     |

---

## 🗂️ Project Structure

```
📦 project/
├── app/
│   ├── main.py
│   ├── models.py
│   ├── database.py
│   ├── auth.py
│   ├── rbac.py
│   ├── routes/
│   └── initial_setup.py
├── streamlit_ui/
│   ├── main.py
│   ├── login.py
│   ├── signup.py
│   ├── admin_panel.py
│   ├── librarian_panel.py
│   ├── member_panel.py
│   ├── update_profile.py
│   └── book_panel.py
```

---

## ⚙️ Setup Instructions

### 🔧 Backend

1. **Clone the repo**  
   ```bash
   git clone https://github.com/your-username/library-management.git
   cd library-management
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure `.env`**
   ```env
   DATABASE_URL=postgresql://username:password@localhost:5432/library_db
   ```

5. **Run the FastAPI server**
   ```bash
   uvicorn app.main:app --reload
   ```

---

### 💻 Frontend (Streamlit)

1. Navigate to the `streamlit_ui` folder:
   ```bash
   cd streamlit_ui
   ```

2. Run the Streamlit app:
   ```bash
   streamlit run main.py
   ```

---

## 🔐 Default Admin Credentials

| Email             | Password   |
|------------------|------------|
| admin@example.com| adminpass  |

---

## 📘 API Overview

| Endpoint | Method | Access | Description |
|----------|--------|--------|-------------|
| `/users/signup` | POST | Public | Register a member |
| `/users/login` | POST | Public | Login and receive JWT |
| `/books/books_list/` | GET | All | View available books |
| `/borrowings/borrow_book/{id}` | POST | Member | Borrow a book |
| `/borrowings/return_book/{id}` | POST | Member | Request return |
| `/borrowings/approve_return/{id}` | POST | Librarian | Approve return |
| `/users/promote/{user_id}` | PUT | Admin | Promote user to librarian/admin |
| `/add_access/` | POST | Admin | Add new role permission |

---

## 🌱 Future Enhancements
- Email notifications (due dates, late returns)
- Mobile responsive design
- Book recommendation engine
- QR code-based check-in/out

---

## 📬 License & Author

Built with ❤️ by **Rajiv Singh**  
MIT License – feel free to fork, extend, and contribute!
