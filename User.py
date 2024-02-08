import json
import uuid
from datetime import datetime, timedelta

class User:
    def __init__(self, users_file, books_file):
        self.users_file = users_file
        self.books_file = books_file
        self.load_initial_data()

    def load_initial_data(self):
        # Load data from JSON files
        with open(self.users_file, 'r') as file:
            self.users = json.load(file)
        with open(self.books_file, 'r') as file:
            self.books = json.load(file)
        self.current_user = None

    def save_data(self):
        # Save updated data back to JSON files
        with open(self.users_file, 'w') as users_file:
            json.dump(self.users, users_file, indent=4)
        with open(self.books_file, 'w') as books_file:
            json.dump(self.books, books_file, indent=4)

    def signup(self, username):
        # Create a new user with a unique ID and token
        user_id = str(uuid.uuid4())
        token = str(uuid.uuid4())
        self.users["users"][user_id] = {
            "username": username,
            "token": token,
            "books_borrowed": {},
            "fines": 0
        }
        self.save_data()
        print(f"User '{username}' created successfully. Your user ID is {user_id} and your token is {token}.")

    def login(self, user_id, token):
        # Authenticate user by ID and token
        if user_id in self.users["users"] and self.users["users"][user_id]["token"] == token:
            self.current_user = user_id
            print(f"Login successful. Welcome, {self.users['users'][user_id]['username']}")
            return True
        else:
            print("Invalid user ID or token.")
            return False

    def borrow_book(self):
        # Allow the user to borrow a book if available
        self.display_available_books()
        book_id_or_title = input("Enter book ID or title to borrow: ").strip()
        # Find book by ID or title
        book_id = self.find_book_id_by_title(book_id_or_title)
        if book_id and self.books[book_id]["available"] > 0:
            self.process_borrow(book_id)
        else:
            print("Book not available for borrowing.")

    def find_book_id_by_title(self, book_id_or_title):
        # Helper method to find book ID by title
        if book_id_or_title.isdigit() and book_id_or_title in self.books:
            return book_id_or_title
        for book_id, book_info in self.books.items():
            if book_info["title"].lower() == book_id_or_title.lower():
                return book_id
        return None

    def process_borrow(self, book_id):
        # Process book borrowing
        current_date = datetime.now().strftime('%Y-%m-%d')
        due_date = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')
        borrowed_book_info = {
            "title": self.books[book_id]["title"],
            "author": self.books[book_id]["author"],
            "borrowed_date": current_date,
            "due_date": due_date,
            "count": 1  # Assuming borrowing one copy at a time
        }
        user_borrowed_books = self.users["users"][self.current_user]["books_borrowed"]
        if book_id in user_borrowed_books:
            user_borrowed_books[book_id]["count"] += 1
        else:
            user_borrowed_books[book_id] = borrowed_book_info
        self.books[book_id]["available"] -= 1
        self.save_data()
        print(f"Book '{self.books[book_id]['title']}' borrowed successfully. Due date: {due_date}.")

    def display_available_books(self):
        # Display all available books for borrowing
        print("Available Books:")
        for book_id, book_info in self.books.items():
            if book_info["available"] > 0:
                print(f"Book ID: {book_id}, Title: {book_info['title']}, Author: {book_info['author']}, Available: {book_info['available']}")

    def return_book(self):
        # Allow the user to return a borrowed book
        self.view_borrowed_books()
        book_id = input("Enter book ID to return: ").strip()
        if book_id in self.users["users"][self.current_user]["books_borrowed"]:
            self.process_return(book_id)
        else:
            print("Invalid book ID or book not borrowed by you.")

    def process_return(self, book_id):
        # Process book returning
        self.books[book_id]["available"] += 1
        user_borrowed_books = self.users["users"][self.current_user]["books_borrowed"]
        user_borrowed_books[book_id]["count"] -= 1
        if user_borrowed_books[book_id]["count"] == 0:
            del user_borrowed_books[book_id]
        self.save_data()
        print(f"Book '{self.books[book_id]['title']}' returned successfully.")

    def view_borrowed_books(self):
        # Display all books currently borrowed by the user
        if self.current_user:
            borrowed_books = self.users["users"][self.current_user]["books_borrowed"]
            if borrowed_books:
                print("Borrowed Books:")
                for book_id, book_info in borrowed_books.items():
                    print(f"Book ID: {book_id}, Title: {book_info['title']}, Author: {book_info['author']}, Borrowed Date: {book_info['borrowed_date']}, Due Date: {book_info['due_date']}, Count: {book_info['count']}")
            else:
                print("No books currently borrowed.")
        else:
            print("Please login to view borrowed books.")
