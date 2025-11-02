# db.py
from __future__ import annotations
import os
from typing import List, Dict, Any, Optional
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from contextlib import contextmanager
from dotenv import load_dotenv

load_dotenv()

_engine: Optional[Engine] = None


def get_engine() -> Engine:
    global _engine
    if _engine is None:
        _engine = create_engine(os.environ["DATABASE_URL"], pool_pre_ping=True)
    return _engine


@contextmanager
def conn():
    e = get_engine()
    with e.begin() as c:
        yield c


def insert_employees(rows: List[Dict[str, Any]]) -> None:
    sql = text("""
        INSERT INTO employees (
            employee_id, name, lastname, email, phone_number, position, department,
            skills, location, hire_date, supervisor, salary
        ) VALUES (
            :employee_id, :name, :lastname, :email, :phone_number, :position, :department,
            CAST(:skills AS JSONB), :location, :hire_date, :supervisor, :salary
        )
        ON CONFLICT (email) DO NOTHING
    """)
    with conn() as c:
        c.execute(sql, rows)


def get_employee_by_email(email: str) -> Optional[Dict[str, Any]]:
    with conn() as c:
        r = c.execute(text("SELECT * FROM employees WHERE email=:e"),
                      {"e": email}).mappings().first()
        return dict(r) if r else None
