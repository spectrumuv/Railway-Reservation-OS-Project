import socket

def main():
    # Create a socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Set up the server address
    server_address = ('127.0.0.1', 38986)  # Change to the server's IP and port
    client_socket.connect(server_address)

    while True:
        print("Menu:\n1. Admin Mode\n2. User Mode\n3. Exit\nEnter your choice:", end=" ")
        choice = int(input())

        if choice == 1:
            admin_password = input("Enter admin password: ")
            if admin_password == "admin":
                while True:
                    print("Admin Options:\n1. Register Train\n2. Delete Train\n3. Logout\nEnter your choice:", end=" ")
                    admin_option = int(input())

                    if admin_option == 1:
                        # Implement registering train functionality
                        train_number = input("Enter train number: ")
                        hours_taken = input("Enter hours taken: ")
                        destination_station = input("Enter destination station: ")
                        boarding_station = input("Enter boarding station: ")
                        number_of_seats = input("Enter number of seats: ")
                        register_train_command = f"REGISTER_TRAIN {train_number} {hours_taken} {destination_station} {boarding_station} {number_of_seats}"
                        client_socket.send(register_train_command.encode())
                        response = client_socket.recv(1000).decode()
                        print(f"Server Response: {response}")
                    elif admin_option == 2:
                        # Implement deleting train functionality
                        train_number = input("Enter train number to delete: ")
                        delete_train_command = f"DELETE_TRAIN {train_number}"
                        client_socket.send(delete_train_command.encode())
                        response = client_socket.recv(1000).decode()
                        print(f"Server Response: {response}")
                    elif admin_option == 3:
                        break
                    else:
                        print("Invalid option. Try again.")
            else:
                print("Incorrect password. Try again.")
        elif choice == 2:
            print("User Mode:\n1. Login\n2. Register\n3. Exit\nEnter your choice:", end=" ")
            user_choice = int(input())

            if user_choice == 1:
                username = input("Enter username: ")
                password = input("Enter password: ")
                login_command = f"AUTHENTICATE_USER {username} {password}"
                client_socket.send(login_command.encode())
                response = client_socket.recv(1000).decode()
                print(f"Server Response: {response}")

                if response == "Authentication successful.":
                    while True:
                        print("User Options:\n1. Search Trains\n2. Display Tickets\n3. Book Ticket\n4. Cancel Ticket\n5. Display Profile\n6. Update Profile\n7. Logout\nEnter your choice:", end=" ")
                        user_option = int(input())

                        if user_option == 1:
                            search_term = input("Enter search term (boarding or destination station): ").lower()
                            search_command = f"SEARCH_TRAINS {search_term}"
                            client_socket.send(search_command.encode())
                            response = client_socket.recv(1000).decode()
                            if response == "No results found.":
                                print("No results found.")
                            else:
                                print(f"Server Response:\n{response}")
                        elif user_option == 2:
                            username = input("Enter the username to display tickets: ")
                            display_user_tickets_command = f"DISPLAY_USER_TICKETS {username}"
                            client_socket.send(display_user_tickets_command.encode())
                            response = client_socket.recv(4096).decode()
                            print(f"Server Response:\n{response}")
                        elif user_option == 3:
                            username = input("Enter your username: ")
                            train_number = input("Enter the train number: ")
                            book_ticket_command = f"BOOK_TICKET {username} {train_number}"
                            client_socket.send(book_ticket_command.encode())
                            response = client_socket.recv(1000).decode()
                            print(f"Server Response: {response}")
                        elif user_option == 4:
                        # Cancel Ticket
                            username = input("Enter your username: ")
                            train_number = input("Enter the train number for the ticket to cancel: ")
                            cancel_ticket_command = f"CANCEL_TICKET {username} {train_number}"
                            client_socket.send(cancel_ticket_command.encode())
                            response = client_socket.recv(1000).decode()
                            print(f"Server Response: {response}") 
                        elif user_option == 5:
                            username = input("Enter your username: ")
                            display_profile_command = f"DISPLAY_PROFILE {username}"
                            client_socket.send(display_profile_command.encode())
                            response = client_socket.recv(1000).decode()
                            print(f"Server Response:\n{response}")

                        elif user_option == 6:
                            username = input("Enter your username: ")
                            new_age = input("Enter new age (leave blank to keep unchanged): ")
                            new_mobile_number = input("Enter new mobile number (leave blank to keep unchanged): ")
                            update_profile_command = f"UPDATE_PROFILE {username} {new_age} {new_mobile_number}"
                            client_socket.send(update_profile_command.encode())
                            response = client_socket.recv(1000).decode()
                            print(f"Server Response: {response}")       
                        elif user_option == 7:
                            break
                        else:
                            print("Invalid option. Try again.")
            elif user_choice == 2:
                username = input("Enter username: ")
                password = input("Enter password: ")
                age = int(input("Enter age: "))
                mobile_number = input("Enter mobile number: ")
                full_name = input("Enter full name: ")
                register_command = f"REGISTER_USER {username} {password} {age} {mobile_number} {full_name}"
                client_socket.send(register_command.encode()) 
                print("Sent request")
                response = client_socket.recv(1000).decode()
                print("Received request")
                print(f"Server Response: {response}")
            elif user_choice == 3:
                break
            else:
                print("Invalid option. Try again.")
        elif choice==3:
            break        
        else:
            print("Invalid option. Try again.")

    # Close the client socket
    client_socket.close()

if __name__ == "__main__":
    main()
