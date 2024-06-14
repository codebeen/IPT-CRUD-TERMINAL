import sys
import sqlite3


# main function of the program
def main():
    # calls create_database method to create database
    create_database()

    # calls the read_data() function to display existing data
    read_data()

    # calls input_choice() function to ask for user input
    input_choice()


def create_database():
    connection_str = sqlite3.connect('bookmark_crud.db')  # Connects to the SQLite database named 'bookmark_crud.db'.
    cursor = connection_str.cursor()  # Creates a cursor object which allows you to execute SQL commands.

    # statement to create table in database
    create_table_str = "CREATE TABLE IF NOT EXISTS bookmark (BK_ID INTEGER PRIMARY KEY AUTOINCREMENT, Title TEXT NOT NULL, URL TEXT NOT NULL)"
    cursor.execute(create_table_str)

    # checks if table is empty
    # Execute a query to count the number of rows in the table.
    cursor.execute(f"SELECT COUNT(*) FROM bookmark")
    count = cursor.fetchone()[0]  # Fetch the result and get the count.

    if count == 0:
        # Insert sample data into the table for testing.
        cursor.execute(
            "INSERT INTO bookmark (Title, URL) VALUES ('Programming in Python 3', 'https://www.qtrac.eu/py3book.html')")
        cursor.execute("INSERT INTO bookmark (Title, URL) VALUES ('Python', 'https://www.python.org/')")
        cursor.execute("INSERT INTO bookmark (Title, URL) VALUES ('PyQt', 'https://www.riverbankcomputing.com/')")
        cursor.execute("INSERT INTO bookmark (Title, URL) VALUES ('Qtrac Ltd', 'https://www.qtrac.eu/')")
        cursor.execute("INSERT INTO bookmark (Title, URL) VALUES ('Scientific Tools for Python', 'https://scipy.org/')")

        connection_str.commit()  # Saves the changes made to the database.

    # close the cursor
    cursor.close
    connection_str.close()  # close the connection


def input_choice():
    # loop if invalid input
    while True:
        # ask for user input
        choice = input("(A)dd (E)dit (L)ist (R)emove (Q)uit: ").upper()

        if choice == "A":
            add_data()
            break
        elif choice == "E":
            edit_data()
            break
        elif choice == "L":
            read_data()
            break
        elif choice == "R":
            delete_data()
            break
        elif choice == "Q":
            print("Program exiting...")
            sys.exit(0)
        else:
            print("Invalid input! Please choose between A, E, L, R, or Q.")
            input_choice()  # ask again for choice


def add_data():
    while True:
        bookmark_title = input("Enter Bookmark Title: ").capitalize().strip()
        if not bookmark_title:
            print("Bookmark title cannot be empty. Please try again.")
            continue

        while True:
            bookmark_url = input("Enter Bookmark URL: ").strip()
            if not bookmark_url:
                print("Bookmark URL cannot be empty. Please try again.")
                continue
            break # exits while loop

        break # exits while loop

    connection_str = sqlite3.connect('bookmark_crud.db')  # Connects to the SQLite database named 'bookmark_crud.db'.
    cursor = connection_str.cursor()  # Creates a cursor object which allows you to execute SQL commands.

    # Execute the INSERT statement with parameterized values
    cursor.execute("INSERT INTO bookmark (Title, URL) VALUES (?, ?)", (bookmark_title, bookmark_url))

    # commit() method to save changes to the database
    connection_str.commit()

    cursor.close()
    connection_str.close()
    print("Successfully added!")


def read_data():
    connection_str = sqlite3.connect('bookmark_crud.db')  # Connects to the SQLite database named 'bookmark_crud.db'.
    cursor = connection_str.cursor()  # Creates a cursor object which allows you to execute SQL commands.

    # select statement to read data from the table
    select_query = "SELECT * FROM bookmark"

    # execute() method use to run SQL query
    cursor = connection_str.execute(select_query)

    # fetchall() method to fetch the data
    records = cursor.fetchall()

    for record in records:
        print(record)

    # close the cursor
    cursor.close()
    connection_str.close()


def edit_data():
    bookmark_no = input("Number of Bookmark to edit: ")  # Prompts the user to input the ID of the item to edit.

    connection_str = sqlite3.connect('bookmark_crud.db')  # Connects to the SQLite database named 'bookmark_crud.db'.
    cursor = connection_str.cursor()  # Creates a cursor object which allows you to execute SQL commands.

    # Fetch existing data to display to the user.
    cursor.execute("SELECT * FROM bookmark WHERE BK_ID = ?", (bookmark_no,))
    item = cursor.fetchone()  # Retrieves the row with the specified ID.

    if item:  # If an item with the given ID exists.

        new_url = input(f"URL [{item[2]}]: ")
        new_title = input(f"Title [{item[1]}]: ")

        if not new_url:  # If the user leaves the url blank, retain the current url.
            new_url = item[2]
        if not new_title:  # If the user leaves the title blank, retain the current title.
            new_title = item[1]
        else:
            new_url = new_url
            new_title = new_title

        cursor.execute("UPDATE bookmark SET TItle = ?, URL = ? WHERE BK_ID = ?",
                       (new_title, new_url, bookmark_no))  # Update the row with the new values.

        connection_str.commit()  # Saves the changes made to the database.
        print("Item updated successfully.")
    else:
        print("Item with the specified ID does not exist.")

    cursor.close()
    connection_str.close()


def delete_data():

    bookmark_no = input("Enter the bookmark number you want to delete: ")  # Prompt the user for the item ID.

    connection_str = sqlite3.connect('bookmark_crud.db')  # Connects to the SQLite database named 'bookmark_crud.db'.
    cursor = connection_str.cursor()  # Create a cursor object.

    # Fetch existing data to confirm deletion with the user.
    cursor.execute("SELECT * FROM bookmark WHERE BK_ID = ?", (bookmark_no,))
    item = cursor.fetchone()  # Retrieve the row with the specified ID.

    if item:  # If an item with the given ID exists.
        print(f"Current data: ID = {item[0]}, Title = {item[1]}, URL = {item[2]}")
        confirm = input("Are you sure you want to delete this item? (yes/no): ")

        if confirm.lower() == "yes":
            cursor.execute("DELETE FROM bookmark WHERE BK_ID = ?", (bookmark_no,))  # Delete the row with the specified ID.
            connection_str.commit()  # Save the changes to the database.
            print("Item deleted successfully.")
        elif confirm.lower() == "no":
            print("Deletion cancelled.")
        else:
            print("Invalid input! Please enter yes/no.")
    else:
        print("Item with the specified ID does not exist.")

    cursor.close()
    connection_str.close()  # Close the database connection.



# call main function to start the program
main()