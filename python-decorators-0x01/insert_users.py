import sqlite3

# Connect to the existing database
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Sample user data
users = [
    ('Alice Johnson', 'alice@example.com'),
    ('Bob Smith', 'bob@example.com'),
    ('Carol Davis', 'carol@example.com'),
    ('David Wilson', 'david@example.com'),
    ('Eva Brown', 'eva@example.com'),
    ('Frank Moore', 'frank@example.com'),
    ('Grace Taylor', 'grace@example.com'),
    ('Henry Anderson', 'henry@example.com'),
    ('Ivy Thomas', 'ivy@example.com'),
    ('Jack White', 'jack@example.com')
]

# Insert users into the table
cursor.executemany('''
    INSERT INTO users (username, email, password)
    VALUES (?, ?, ?)
''', [(username, email, 'default123') for username, email in users])

# Commit and close
conn.commit()
conn.close()

print("10 users inserted successfully.")
