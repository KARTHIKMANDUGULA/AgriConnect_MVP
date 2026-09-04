import sqlite3

def create_database():
    # Connects to your SSD and creates the physical file
    conn = sqlite3.connect('agriconnect.db')
    cursor = conn.cursor()

    # TABLE 1: USERS
    # 'id' is the Primary Key. AUTOINCREMENT means it automatically assigns 1, 2, 3...
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )
    ''')

    # TABLE 2: INVENTORY
    # 'id' is the Primary Key for the crop. 
    # 'farmer_username' is the Relationship linking back to the Users table.
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        farmer_username TEXT NOT NULL,
        crop_name TEXT NOT NULL,
        price_per_kg INTEGER NOT NULL,
        stock_kg INTEGER NOT NULL,
        emoji TEXT
    )
    ''')

    # Insert secure mock data to prove the backend works
    try:
        cursor.execute("INSERT INTO Users (username, password, role) VALUES ('ramesh', 'pass123', 'Farmer')")
        cursor.execute("INSERT INTO Users (username, password, role) VALUES ('anita', 'buyer123', 'Customer')")
    except sqlite3.IntegrityError:
        pass # Skips if Ramesh and Anita are already registered

    # Save and close
    conn.commit()
    conn.close()
    print("✅ Database 'agriconnect.db' created successfully with Primary Keys and Relationships!")

if __name__ == "__main__":
    create_database()