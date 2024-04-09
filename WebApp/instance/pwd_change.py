import sqlite3

# Connect to the database
conn = sqlite3.connect('database.db')

try:
    # Prompt user for new password
    new_password = input("Enter the new password: ")

    # Create a cursor object
    cursor = conn.cursor()

    # Execute SQL query to update the password for the specified email
    cursor.execute("UPDATE user SET password = ? WHERE email = ?;", (new_password, 'sami.masmoudi@etudiant-enit.utm.tn'))

    # Commit the transaction
    conn.commit()

    # Check if any rows were updated
    if cursor.rowcount > 0:
        print("Password updated successfully.")
    else:
        print("No user found with the specified email.")

except sqlite3.Error as e:
    print("Error:", e)

finally:
    # Close the connection
    conn.close()
