import sqlite3

# Connect to the database
conn = sqlite3.connect('database.db')

try:
    # Create a cursor object
    cursor = conn.cursor()

    # Execute SQL query to list all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

    # Fetch results
    tables = cursor.fetchall()

    if tables:
        # Print the list of tables
        for table in tables:
            print(table[0])
    else:
        print("No tables found in the database.")

except sqlite3.Error as e:
    print("Error:", e)

finally:
    # Close the connection
    conn.close()
