import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), "edupathx.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS bkt_parameters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    concept_id INTEGER UNIQUE NOT NULL,
    p_init FLOAT DEFAULT 0.20,
    p_trans FLOAT DEFAULT 0.15,
    p_slip FLOAT DEFAULT 0.10,
    p_guess FLOAT DEFAULT 0.25,
    sample_size INTEGER DEFAULT 0,
    last_calibrated DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()
conn.close()
print("bkt_parameters table ensured.")
