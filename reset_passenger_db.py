import sqlite3

conn = sqlite3.connect("bus_passenger.db")
cursor = conn.cursor()

# Delete old passengers table
cursor.execute("DROP TABLE IF EXISTS passengers")

# Recreate passengers table with phone_number
cursor.execute('''
CREATE TABLE passengers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    image_path TEXT NOT NULL,
    start_stop TEXT NOT NULL,
    destination_stop TEXT NOT NULL,
    phone_number TEXT NOT NULL
)
''')

# Insert clean passengers
passengers = [
    ("jithisha", r"C:\Users\jithi\OneDrive\Documents\C-Free\Temp\aa.jpg", "eathencadu", "acew", "+918637484291"),
    ("dhanya", r"C:\Users\jithi\OneDrive\Documents\C-Free\Temp\dd.jpg", "Central Station", "North Avenue", "+919812345678"),
    ("deepsi", r"C:\Users\jithi\OneDrive\Documents\C-Free\Temp\bb.jpg", "West End", "East Park", "+919811112222"),
    ("abinaya", r"C:\Users\jithi\OneDrive\Documents\C-Free\Temp\pp.jpg", "South Street", "City Square", "+917358887224")
]

cursor.executemany('''
INSERT INTO passengers (name, image_path, start_stop, destination_stop, phone_number) 
VALUES (?, ?, ?, ?, ?)
''', passengers)

conn.commit()
conn.close()

print("✅ Passengers table reset with clean data!")
