import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), "edupathx.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get existing columns in questions
cursor.execute("PRAGMA table_info(questions)")
columns = [col[1] for col in cursor.fetchall()]

new_cols = [
    ("starter_code", "TEXT"),
    ("test_cases", "JSON"),
    ("calibrated_slip", "FLOAT"),
    ("calibrated_guess", "FLOAT"),
    ("calibrated_difficulty", "FLOAT")
]

for col_name, col_type in new_cols:
    if col_name not in columns:
        print(f"Adding column {col_name} to questions table...")
        cursor.execute(f"ALTER TABLE questions ADD COLUMN {col_name} {col_type}")

conn.commit()
conn.close()
print("Migration completed.")
