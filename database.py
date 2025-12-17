import sqlite3

DB_NAME = "production.db"

def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS production_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        machine_id TEXT,
        paper_type TEXT,
        run_size_class TEXT,
        max_speed REAL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS deviations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        machine_id TEXT,
        current_speed REAL,
        reference_speed REAL,
        deviation_percent REAL,
        category TEXT,
        technical_issue TEXT,
        informed_party TEXT,
        comment TEXT
    )
    """)

    conn.commit()
    conn.close()

def get_reference_speed(machine_id, paper_type, run_size_class):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT MAX(max_speed)
        FROM production_history
        WHERE machine_id = ?
        AND paper_type = ?
        AND run_size_class = ?
    """, (machine_id, paper_type, run_size_class))

    result = cur.fetchone()[0]
    conn.close()
    return result

def store_deviation(data):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO deviations
        (machine_id, current_speed, reference_speed, deviation_percent,
         category, technical_issue, informed_party, comment)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["machine_id"],
        data["current_speed"],
        data["reference_speed"],
        data["deviation_percent"],
        data["category"],
        data.get("technical_issue"),
        data.get("informed_party"),
        data.get("comment")
    ))

    conn.commit()
    conn.close()
