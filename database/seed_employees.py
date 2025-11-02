from data.employees import generate_employee_data
from database.db import insert_employees
import uuid
import json


def main():
    employees = generate_employee_data(50)
    for e in employees:
        e["employee_id"] = str(uuid.uuid4())
        e["skills"] = json.dumps(e["skills"])  # store list as JSONB text
    insert_employees(employees)
    print("✅ Seeded 50 employees successfully.")


if __name__ == "__main__":
    main()
