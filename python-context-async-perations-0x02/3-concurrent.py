import aiosqlite
import asyncio

# Fetch all users
async def async_fetch_users():
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            users = await cursor.fetchall()
            return users

# Fetch users older than 40
async def async_fetch_older_users():
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            older_users = await cursor.fetchall()
            return older_users

# Run both queries concurrently and return results
async def fetch_concurrently():
    all_users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    return all_users, older_users

# Execute and print results
all_users, older_users = asyncio.run(fetch_concurrently())

print("All Users:")
for user in all_users:
    print(user)

print("\nUsers Older Than 40:")
for user in older_users:
    print(user)
