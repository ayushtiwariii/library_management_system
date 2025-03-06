import mysql.connector
from tabulate import tabulate

# Database Connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="206677",
    database="LibraryDB"
)
cursor = conn.cursor()

# Function to Display Header
def display_header():
    print("="*50)
    print("📚 LIBRARY MANAGEMENT SYSTEM 📚".center(50))
    print("="*50)

# Admin Authentication
def admin_login():
    display_header()
    username = input("Enter admin username: ")
    password = input("Enter admin password: ")
    cursor.execute("SELECT * FROM Admins WHERE username=%s AND password=%s", (username, password))
    if cursor.fetchone():
        print("✅ Login successful!\n")
        return True
    else:
        print("❌ Invalid credentials!\n")
        return False

# Display Books in Tabular Format
def view_books():
    cursor.execute("SELECT * FROM Books")
    books = cursor.fetchall()
    if books:
        print(tabulate(books, headers=["ID", "Title", "Author", "Available"], tablefmt="grid"))
    else:
        print("📌 No books found.")

# Display Students in Tabular Format
def view_students():
    cursor.execute("SELECT * FROM Students")
    students = cursor.fetchall()
    if students:
        print(tabulate(students, headers=["ID", "Name", "Email"], tablefmt="grid"))
    else:
        print("📌 No students found.")

# Book Management
def add_book():
    display_header()
    title = input("Enter Book Title: ")
    author = input("Enter Book Author: ")
    cursor.execute("INSERT INTO Books (title, author) VALUES (%s, %s)", (title, author))
    conn.commit()
    print("✅ Book added successfully!")

def remove_book():
    display_header()
    view_books()
    book_id = input("Enter Book ID to remove: ")
    cursor.execute("DELETE FROM Books WHERE book_id=%s", (book_id,))
    conn.commit()
    print("✅ Book removed successfully!")

def search_book():
    display_header()
    title = input("Enter Book Title to search: ")
    cursor.execute("SELECT * FROM Books WHERE title LIKE %s", (f"%{title}%",))
    books = cursor.fetchall()
    if books:
        print(tabulate(books, headers=["ID", "Title", "Author", "Available"], tablefmt="grid"))
    else:
        print("❌ No matching books found.")

# Student Management
def add_student():
    display_header()
    name = input("Enter Student Name: ")
    email = input("Enter Student Email: ")
    cursor.execute("INSERT INTO Students (name, email) VALUES (%s, %s)", (name, email))
    conn.commit()
    print("✅ Student added successfully!")

def remove_student():
    display_header()
    view_students()
    student_id = input("Enter Student ID to remove: ")
    cursor.execute("DELETE FROM Students WHERE student_id=%s", (student_id,))
    conn.commit()
    print("✅ Student removed successfully!")

def search_student():
    display_header()
    name = input("Enter Student Name to search: ")
    cursor.execute("SELECT * FROM Students WHERE name LIKE %s", (f"%{name}%",))
    students = cursor.fetchall()
    if students:
        print(tabulate(students, headers=["ID", "Name", "Email"], tablefmt="grid"))
    else:
        print("❌ No matching students found.")

# Issuing & Returning Books
def issue_book():
    display_header()
    view_books()
    book_id = input("Enter Book ID: ")
    view_students()
    student_id = input("Enter Student ID: ")
    cursor.execute("SELECT available FROM Books WHERE book_id=%s", (book_id,))
    book = cursor.fetchone()
    
    if book and book[0]:  # Check availability
        cursor.execute("INSERT INTO IssuedBooks (book_id, student_id) VALUES (%s, %s)", (book_id, student_id))
        cursor.execute("UPDATE Books SET available=FALSE WHERE book_id=%s", (book_id,))
        conn.commit()
        print("✅ Book issued successfully!")
    else:
        print("❌ Book is not available!")

def return_book():
    display_header()
    book_id = input("Enter Book ID: ")
    cursor.execute("UPDATE Books SET available=TRUE WHERE book_id=%s", (book_id,))
    cursor.execute("UPDATE IssuedBooks SET return_date=NOW() WHERE book_id=%s AND return_date IS NULL", (book_id,))
    conn.commit()
    print("✅ Book returned successfully!")

# Main Menu
if admin_login():
    while True:
        display_header()
        print("1️⃣  Add Book")
        print("2️⃣  Remove Book")
        print("3️⃣  View Books")
        print("4️⃣  Search Book")
        print("5️⃣  Add Student")
        print("6️⃣  Remove Student")
        print("7️⃣  View Students")
        print("8️⃣  Search Student")
        print("9️⃣  Issue Book")
        print("🔟  Return Book")
        print("0️⃣  Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            add_book()
        elif choice == "2":
            remove_book()
        elif choice == "3":
            view_books()
        elif choice == "4":
            search_book()
        elif choice == "5":
            add_student()
        elif choice == "6":
            remove_student()
        elif choice == "7":
            view_students()
        elif choice == "8":
            search_student()
        elif choice == "9":
            issue_book()
        elif choice == "10":
            return_book()
        elif choice == "0":
            print("📌 Exiting system...")
            break
        else:
            print("❌ Invalid choice! Please try again.")

# Close Connection
cursor.close()
conn.close()
