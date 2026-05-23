import sqlite3

DB_NAME = "growth_tracker.db"

def connect():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def create_table():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS daily_entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        entry_date TEXT UNIQUE,
        mood INTEGER,
        energy INTEGER,
        productivity INTEGER,
        sleep_hours REAL,
        study_hours REAL,
        workout INTEGER,
        health_status TEXT,
        opportunities_gained INTEGER,
        opportunities_missed INTEGER,
        notes TEXT,
        golden_day INTEGER DEFAULT 0,
        growth_score REAL
    )
    """)

    # ✅ Migration — safely add golden_day if it doesn't exist yet
    try:
        cur.execute("ALTER TABLE daily_entries ADD COLUMN golden_day INTEGER DEFAULT 0")
        conn.commit()
    except Exception:
        pass  # Column already exists — no problem

    conn.commit()
    conn.close()

def insert_entry(data):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    INSERT OR REPLACE INTO daily_entries (
        entry_date, mood, energy, productivity, sleep_hours,
        study_hours, workout, health_status, opportunities_gained,
        opportunities_missed, notes, golden_day, growth_score
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, data)

    conn.commit()
    conn.close()

def fetch_entries():
    conn = connect()
    cur = conn.cursor()

    # ✅ Explicit column order — always returns 14 columns in correct order
    cur.execute("""
        SELECT id, entry_date, mood, energy, productivity, sleep_hours,
               study_hours, workout, health_status, opportunities_gained,
               opportunities_missed, notes, golden_day, growth_score
        FROM daily_entries
        ORDER BY entry_date ASC
    """)
    rows = cur.fetchall()

    conn.close()
    return rows