# This will manage hashing and database lookups.

import os
import uuid
import bcrypt
from sqlalchemy import text
from database.db import get_engine


def hash_password(password: str) -> str:
    # bcrypt supports max 72 bytes — truncate to be safe
    password_bytes = password.encode("utf-8")[:72]
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password_bytes, salt).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8")[:72],
            hashed_password.encode("utf-8")
        )
    except Exception:
        return False


def get_user_by_email(email: str):
    engine = get_engine()
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT * FROM users WHERE email = :email"), {"email": email}).fetchone()
        return dict(result._mapping) if result else None


def create_user(email: str, password: str, employee_id: str):
    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO users (id, email, password_hash, employee_id)
                VALUES (:id, :email, :password_hash, :employee_id)
            """),
            {
                "id": str(uuid.uuid4()),
                "email": email,
                "password_hash": hash_password(password),
                "employee_id": employee_id,
            },
        )
