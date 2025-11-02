# Handles first-time registration (based on existing employee record).

import streamlit as st
from sqlalchemy import text
from database.db import get_engine
from auth.auth_utils import create_user, get_user_by_email


def signup():
    st.subheader("🆕 Employee Registration")
    email = st.text_input("Corporate Email")
    password = st.text_input("Set Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Sign Up"):
        if password != confirm_password:
            st.error("Passwords do not match.")
            return

        engine = get_engine()
        with engine.connect() as conn:
            employee = conn.execute(text("SELECT employee_id FROM employees WHERE email = :email"), {
                                    "email": email}).fetchone()

        if not employee:
            st.error("No employee record found for this email. Contact HR.")
            return

        if get_user_by_email(email):
            st.warning("User already exists. Please log in instead.")
            return

        create_user(email, password, employee.employee_id)
        st.success("✅ Registration successful! You can now log in.")
