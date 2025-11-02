def log_attendance_to_db(attendance_dict):
    conn = sqlite3.connect('passenger.db')
    cursor = conn.cursor()

    # Create attendance table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            status TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Insert each attendance record
    for name, status in attendance_dict.items():
        cursor.execute('''
            INSERT INTO attendance (name, status) VALUES (?, ?)
        ''', (name, status))

    conn.commit()
    conn.close()
    print("📥 Attendance successfully logged into the database.")
