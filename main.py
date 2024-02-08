from admin import Admin
from User import User

def main():
    # Initialize Admin with predefined credentials
    admin_name = "admin"
    admin_password = "admin123"
    admin = Admin(admin_name, admin_password)

    # Specify the paths to the users and books JSON files
    users_file = "/Users/rish/Desktop/1/Library Management System using Python/users.json"
    books_file = "/Users/rish/Desktop/1/Library Management System using Python/books.json"
    user_manager = User(users_file, books_file)

    print("\t\t\t\tWelcome to the Library Management System...!")
    print("1. Admin")
    print("2. User")
    user_type = input("Select user type: ")

    if user_type == "1":
        admin_name_input = input("Enter admin name: ")
        admin_password_input = input("Enter admin password: ")
        if admin.authenticate(admin_name_input, admin_password_input):
            print("Admin authenticated successfully.")
            while True:
                print("\n1. Add Book")
                print("2. View Books")
                print("3. Update Book Information")
                print("4. Remove Book")
                print("5. Create User Account")
                print("6. View User Information")
                print("9. Exit")
                admin_choice = input("Select option: ")
                
                if admin_choice == "1":
                    title = input("Enter book title: ")
                    author = input("Enter book author: ")
                    copies = int(input("Enter number of copies: "))
                    genre = input("Please enter the genre of the book (e.g., Fiction, Mystery, Science Fiction): ")
                    admin.add_book(title, author, copies, genre)

                elif admin_choice == "2":
                    admin.display_books()

                elif admin_choice == "3":
                    admin.update_book()

                elif admin_choice == '4':
                    admin.remove()

                elif admin_choice == '5':
                    username = input("Enter Username: ")
                    user_manager.signup(username)

                elif admin_choice == '6':
                    admin.view_all_users_information()

                elif admin_choice == "9":
                    print("Exiting Admin Panel.")
                    break

                else:
                    print("Invalid choice. Please try again.")

        else:
            print("Invalid admin credentials. Access denied.")

    elif user_type == "2":
        print("\n1. Login")
        print("2. Sign Up")
        print("3. Exit")
        user_choice = input("Select option: ")

        if user_choice == "1":
            user_id = input("Enter your user ID: ")
            token = input("Enter your token: ")
            if user_manager.login(user_id, token):
                while True:
                    print("\n1. Borrow Book")
                    print("2. Return Book")
                    print("3. View Borrowed Books")
                    print("4. Logout")
                    user_option = input("Select option: ")

                    if user_option == "1":
                        user_manager.borrow_book()

                    elif user_option == "2":
                        user_manager.return_book()

                    elif user_option == "3":
                        user_manager.view_borrowed_books()

                    elif user_option == "4":
                        print("Logging out...")
                        break

                    else:
                        print("Invalid option. Please try again.")

            else:
                print("Invalid user ID or token. Please try again.")

        elif user_choice == "2":
            username = input("Enter your username: ").strip()
            user_manager.signup(username)

        elif user_choice == "3":
            print("Exiting the Library Management System.")

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
