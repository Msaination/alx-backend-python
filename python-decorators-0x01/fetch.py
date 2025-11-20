import sqlite3

# Connect to the database
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Query all users
cursor.execute("SELECT id, username, email FROM users")
users = cursor.fetchall()

# Display the results
for user in users:
    print(f"ID: {user[0]}, Name: {user[1]}, Email: {user[2]}")

# Close the connection
conn.close()
