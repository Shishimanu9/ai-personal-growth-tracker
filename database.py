import sqlite3

DB_NAME = "growth.db"


def create_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
                   date TEXT,
            mood TEXT,
            energy INTEGER,
            productivity INTEGER,
            sleep REAL,
            study_hours REAL,
            workout TEXT,
            health TEXT,
            opportunities_got INTEGER,
            opportunities_missed INTEGER,
            notes TEXT,
            growth_score REAL
        )
    ''')

    conn.commit()
    conn.close()
def insert_entry(data):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO daily_entries (
            date,
            mood,
            energy,
            productivity,
            sleep,
            study_hours,
            workout,
            health,
            opportunities_got,
                   opportunities_missed,
            notes,
            growth_score
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', data)

    conn.commit()
    conn.close()


def get_all_entries():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM daily_entries")
    rows = cursor.fetchall()

    conn.close()
    return rows