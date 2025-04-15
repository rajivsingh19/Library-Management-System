from app.models import User, AccessControl
from app.auth import encrypt_password
from app.database import SessionLocal
import uuid

def create_default_admin_and_permissions():
    db = SessionLocal()

    # ✅ Create default admin user
    if not db.query(User).filter_by(role="admin").first():
        print("⚙️ No admin found. Creating default admin user...")
        admin_user = User(
            id=uuid.uuid4(),
            username="admin",
            email="admin@example.com",
            password_encrypted=encrypt_password("adminpass"),
            role="admin",
            is_active=True
        )
        db.add(admin_user)
        db.commit()
        print("✅ Default admin created: admin@example.com / adminpass")

    # ✅ Define permissions
    all_permissions = [
        # Admin permissions
        ("admin", "book", "create"),
        ("admin", "book", "read"),
        ("admin", "book", "update"),
        ("admin", "book", "delete"),
        ("admin", "user", "promote"),
        ("admin", "access", "add"),
        ("admin", "access", "read"),
        ("admin", "access", "update"),
        ("admin", "user", "read"),
        ("admin", "user_permission", "add"),
        ("admin", "user_permission", "read"),
        ("admin", "user_permission", "delete"),


        # Member permissions
        ("member", "book", "read"),
        ("member", "book", "borrow"),
        ("member", "book", "return"),

        # Librarian permissions (optional role)
        ("librarian", "book", "create"),
        ("librarian", "book", "read"),
        ("librarian", "book", "update"),
        ("librarian", "book", "delete"),
        ("librarian", "book", "return"),
        ("librarian", "borrowing", "read"),
        ("librarian", "borrowing", "update"),
    ]

    for role, resource, action in all_permissions:
        existing = db.query(AccessControl).filter_by(
            role=role, resource=resource, action=action
        ).first()
        if not existing:
            db.add(AccessControl(role=role, resource=resource, action=action))
    
    db.commit()
    db.close()
    print("✅ AccessControl table initialized.")
