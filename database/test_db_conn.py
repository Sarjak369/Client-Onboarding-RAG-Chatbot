from db import get_engine
from sqlalchemy import text
engine = get_engine()
with engine.connect() as conn:
    # result = conn.execute(text("SELECT version();"))
    result = conn.execute(text("SELECT * from employees;"))
    # ('PostgreSQL 17.2 on x86_64-apple-darwin23.6.0, compiled by Apple clang version 16.0.0 (clang-1600.0.26.4), 64-bit',)
    print(result.fetchone())
