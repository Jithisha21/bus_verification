import sqlite3

def create_database():
    conn = sqlite3.connect("bus_passenger.db")
    cursor = conn.cursor()

    # Create the passengers table with an image_path column
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS passengers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        image_path TEXT NOT NULL,
        start_stop TEXT NOT NULL,
        destination_stop TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()


def add_passenger(name, image_path, start_stop, destination_stop):
    conn = sqlite3.connect("bus_passenger.db")
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO passengers (name, image_path, start_stop, destination_stop) 
    VALUES (?, ?, ?, ?)
    ''',(name=="aa", 
        image_path==r"C:\Users\jithi\OneDrive\Documents\C-Free\Temp\aa.jpg", 
        start_stop=="eathencadu", 
        destination_stop=="acew"))

    conn.commit()
    conn.close()
if __name__ == "__main__":
    create_database()  # Ensure the database is created

    # Add a passenger using a raw string for the image path
    add_passenger(
        name="jithisha", 
        image_path=r"C:\Users\jithi\OneDrive\Documents\C-Free\Temp\aa.jpg", 
        start_stop="eathencadu", 
        destination_stop="acew"
    )
    add_passenger(
        name="dhanya",
        image_path=r"C:\Users\jithi\OneDrive\Documents\C-Free\Temp\dd.jpg",
        start_stop="Central Station",
        destination_stop="North Avenue"
    )

    add_passenger(
        name="deepsi",
        image_path=r"C:\Users\jithi\OneDrive\Documents\C-Free\Temp\bb.jpg",
        start_stop="West End",
        destination_stop="East Park"
    )

    add_passenger(
        name="abinaya",
        image_path=r"C:\Users\jithi\OneDrive\Documents\C-Free\Temp\pp.jpg",
        start_stop="South Street",
        destination_stop="City Square"
    )
    print("Passenger added successfully!")

