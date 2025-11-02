import sqlite3

def view_attendance():
    conn = sqlite3.connect('passenger.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM attendance ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    print("\n📄 Attendance History:")
    for row in rows:
        print(f"ID: {row[0]} | Name: {row[1]} | Status: {row[2]} | Timestamp: {row[3]}")
    conn.close()

if __name__ == "__main__":
    view_attendance()
