import sqlite3
import random

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Fetch all user IDs
cursor.execute("SELECT id FROM users")
user_ids = cursor.fetchall()

# Update each user with a random age between 18 and 65
for (user_id,) in user_ids:
    age = random.randint(18, 65)
    cursor.execute("UPDATE users SET age = ? WHERE id = ?", (age, user_id))

conn.commit()
conn.close()

print("Random ages assigned to all users.")
