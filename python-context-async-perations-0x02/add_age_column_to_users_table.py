import sqlite3

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Add age column if it doesn't exist
cursor.execute("ALTER TABLE users ADD COLUMN age INTEGER")

conn.commit()
conn.close()
print("Age column added to users table successfully.")
