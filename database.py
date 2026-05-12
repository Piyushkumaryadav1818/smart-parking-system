import sqlite3

# DATABASE CONNECT
con = sqlite3.connect("parking.db")
cur = con.cursor()

# USERS TABLE
cur.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
)
""")

# SLOTS TABLE
cur.execute("""
CREATE TABLE IF NOT EXISTS slots(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slot TEXT,
    status TEXT
)
""")

# BOOKINGS TABLE
cur.execute("""
CREATE TABLE IF NOT EXISTS bookings(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    slot TEXT
)
""")

# INSERT SLOTS ONLY FIRST TIME
cur.execute("SELECT COUNT(*) FROM slots")
count = cur.fetchone()[0]

if count == 0:
    slots = ["A1","A2","A3","B1","B2","B3"]
    for s in slots:
        cur.execute("INSERT INTO slots(slot,status) VALUES(?,?)",(s,"Free"))

# 🔥 RESET ALL SLOTS TO FREE (for testing)
cur.execute("UPDATE slots SET status='Free'")
cur.execute("DELETE FROM bookings")

con.commit()
con.close()

print("Database Ready + Slots Reset")