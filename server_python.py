import socket
import threading
import os

# Define global variables
users = []
trains = []
mutex = threading.Semaphore(1)
mutex_user=threading.Semaphore(1)
mutex_train=threading.Semaphore(1)
mutex_booking=threading.Semaphore(1)

# Function to register a user
def register_user(username, password, age, mobile_number, full_name):
    
    with mutex_user:
        with open("users.txt", "a") as file:
                print("Opened users file")
                file.write(f"{username},{password},{age},{mobile_number},{full_name}\n")
           
        users.append(username)

# Function to authenticate a user
def authenticate_user(username, password):
    with mutex_user:
            with open("users.txt") as file:
                for line in file:
                    stored_username, stored_password, *_ = line.strip().split(',')
                    if username == stored_username and password == stored_password:
                        return True
            return False

# Function to register a train
def register_train(train_number, hours_taken, destination_station, boarding_station, number_of_seats):
    with mutex_train:    
        with open("trains.txt", "a") as file:
            file.write(f"{train_number},{hours_taken},{destination_station},{boarding_station},{number_of_seats},0\n")
        trains.append(train_number)


def delete_train(train_number):
    with mutex_train:
        with open("trains.txt", "r") as file:
            lines = file.readlines()
        with open("trains.txt", "w") as file:
            for line in lines:
                if not line.startswith(train_number):
                    file.write(line)
    
    with mutex_booking:
        with open("booking.txt", "r") as file:
            lines = file.readlines()
        with open("booking.txt", "w") as file:
            for line in lines:
                data = line.strip().split(',')
                if data[0] != train_number:
                    file.write(line)


def find_available_seat(train_number):
        booked_seats = set()
    
        with open("booking.txt", "r") as file:
            for line in file:
                data = line.strip().split(',')
                if data[0] == train_number:
                    booked_seats.add(int(data[1]))
    
        total_seats = int([data.split(',')[4] for data in open("trains.txt") if data.startswith(train_number)][0])
        available_seats = set(range(1, total_seats + 1)).difference(booked_seats)
        if available_seats:
            return min(available_seats)
        else:
            return None

# Function to book a ticket
def book_ticket(username, train_number):
    with mutex_train:
        
        train_info = None
        with open("trains.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                train_data = line.strip().split(',')
                if train_data[0] == train_number:
                    train_info = train_data
                    break

        if train_info:
            available_seats = int(train_info[4]) - int(train_info[5])  # Calculate available seats
            if available_seats > 0:
                # Find an available seat number
                seat_number = find_available_seat(train_number)
                if seat_number:
                    with open(f"{username}_{train_number}.txt", "w") as file:
                        file.write(f"User: {username}\n")
                        file.write(f"Train Number: {train_number}\n")
                        file.write(f"Hours Taken: {train_info[1]}\n")
                        file.write(f"Destination Station: {train_info[2]}\n")
                        file.write(f"Boarding Station: {train_info[3]}\n")
                        file.write(f"Number of Seats: {available_seats}\n")
                        file.write(f"Booked Seat Number: {seat_number}\n")

                    # Update booking details in booking.txt file
                    with open("booking.txt", "a") as booking_file:
                        booking_file.write(f"{train_number},{seat_number},{username}\n")

                    # Update the number of booked seats in trains.txt file
                    updated_lines = []
                    for line in lines:
                        train_data = line.strip().split(',')
                        if train_data[0] == train_number:
                            updated_booked_seats = int(train_data[5]) + 1
                            train_data[5] = str(updated_booked_seats)
                            updated_line = ','.join(train_data) + '\n'
                            updated_lines.append(updated_line)
                        else:
                            updated_lines.append(line)

                        with open("trains.txt", "w") as file:
                            file.writelines(updated_lines)
                    return f"Ticket booked successfully. Seat number: {seat_number}"
                else:
                    return "No available seats."
            else:
                return "No available seats."
        else:
            return "Train not found."

def display_user_tickets(username, client_socket):
    user_tickets = [ticket for ticket in os.listdir() if ticket.startswith(f"{username}_") and ticket.endswith(".txt")]
    
    if not user_tickets:
        response = "No tickets found for this user."
    else:
        response = "User Tickets:\n"
        for ticket in user_tickets:
            with open(ticket, "r") as file:
                content = file.read()
                response += f"{content}\n\n"

    client_socket.send(response.encode())

def display_profile(username):
    # Search for user details in users.txt
    with open("users.txt", "r") as file:
        for line in file:
            user_data = line.strip().split(',')
            if user_data[0] == username:
                profile = (
                    f"Username: {user_data[0]}\n"
                    f"Full Name: {user_data[4]}\n"
                    f"Age: {user_data[2]}\n"
                    f"Mobile Number: {user_data[3]}"
                )
                return profile

    return "Profile not found."

def update_profile(username, new_age, new_mobile_number):
    # Update user details in users.txt
    updated_lines = []
    with mutex_user:
        with open("users.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                user_data = line.strip().split(',')
                if user_data[0] == username:
                    user_data[2] = str(new_age) if new_age else user_data[2]
                    user_data[3] = new_mobile_number if new_mobile_number else user_data[3]
                    updated_line = ','.join(user_data) + '\n'
                    updated_lines.append(updated_line)
                else:
                    updated_lines.append(line)

    # Write updated user details back to users.txt
        with open("users.txt", "w") as file:
            file.writelines(updated_lines)

        return "Profile updated successfully."

def cancel_ticket(username, train_number):
    # Remove ticket details from the user's ticket file
    ticket_file = f"{username}_{train_number}.txt"
    try:
        # Remove the user's ticket file
        os.remove(ticket_file)
    except FileNotFoundError:
        pass  # File not found, no need to delete

    # Remove the ticket details from the booking.txt file
    with open("booking.txt", "r+") as booking_file:
        lines = booking_file.readlines()
        booking_file.seek(0)
        for line in lines:
            data = line.strip().split(',')
            if data[0] == train_number and data[2] == username:
                continue  # Skip writing this line back to the file
            booking_file.write(line)
        booking_file.truncate()

    # Update the booked seat count in trains.txt
    with open("trains.txt", "r+") as trains_file:
        lines = trains_file.readlines()
        trains_file.seek(0)
        for line in lines:
            train_data = line.strip().split(',')
            if train_data[0] == train_number:
                updated_booked_seats = max(0, int(train_data[5]) - 1)
                train_data[5] = str(updated_booked_seats)
                updated_line = ','.join(train_data) + '\n'
                trains_file.write(updated_line)
            else:
                trains_file.write(line)
        trains_file.truncate()

    return "Ticket canceled successfully."

# Function to handle client requests
def handle_request(request, client_socket):
    global users, trains
    with mutex:
        command, *args = request.split() 
    
        if command == "REGISTER_USER":
            username, password, age, mobile_number, full_name = args[:5]
            register_user(username, password, int(age), mobile_number, full_name)
            client_socket.send(b"User registered successfully.")
        elif command == "AUTHENTICATE_USER":
            username, password = args[:2]  
            result = authenticate_user(username, password)
            if result:
                client_socket.send(b"Authentication successful.")
            else:
                client_socket.send(b"Authentication failed.")
        elif command == "REGISTER_TRAIN":
            print("Command register train")
            register_train(*args)
            client_socket.send(b"Train registered successfully.")
        elif command == "DELETE_TRAIN":
            train_number = args[0]
            delete_train(train_number)
            client_socket.send(b"Train deleted successfully.")  
        elif command == "SEARCH_TRAINS":
            search_term = args[0].lower()
            matched_trains_info = []
            for line in open("trains.txt", "r"):
                train_info = line.strip().split(',')
                boarding_station = train_info[3].lower()
                destination_station = train_info[2].lower()
                if search_term in boarding_station or search_term in destination_station:
                    available_seats = int(train_info[4]) - int(train_info[5])  # Calculate available seats
                    matched_trains_info.append((train_info, available_seats))

            if not matched_trains_info:
                client_socket.send(b"No results found.")
            else:
                response = "Matched Trains and Available Seats:\n"
                for train, available_seats in matched_trains_info:
                    response += f"Train Number: {train[0]}\n"
                    response += f"Hours Taken: {train[1]}\n"
                    response += f"Destination Station: {train[2]}\n"
                    response += f"Boarding Station: {train[3]}\n"
                    response += f"Available Seats: {available_seats}\n\n"

            client_socket.send(response.encode())
        elif command == "BOOK_TICKET":
            book_ticket(*args)
            client_socket.send(b"Ticket booked successfully.")
        elif command == "DISPLAY_USER_TICKETS":
            username = args[0]
            display_user_tickets(username, client_socket)  
        elif command == "DISPLAY_PROFILE":
            username = args[0]
            profile = display_profile(username)
            client_socket.send(profile.encode())     
        elif command == "UPDATE_PROFILE":
            username, new_age, new_mobile_number = args[:3]
            update_result = update_profile(username, int(new_age), new_mobile_number)
            client_socket.send(update_result.encode())    
        elif command == "CANCEL_TICKET":
            username, train_number = args[:2]
            cancellation_result = cancel_ticket(username, train_number)
            client_socket.send(cancellation_result.encode())     
        
        else:
            client_socket.send(b"Invalid command.")

def handle_client(client_socket):
    while True:
        try:
            request = client_socket.recv(1000).decode()
            if not request:
                break  # Break the loop if no request received

            handle_request(request, client_socket)
        except Exception as e:
            print(f"Error handling client request: {str(e)}")
            break

    # Close the client socket when done
    client_socket.close()


# Function to start the server
def start_server(port):
    # Create a socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(5)

    # Accept incoming connections and handle requests in separate threads
    while True:
        client_socket, _ = server_socket.accept()

        # Create a new thread for each client request
        threading.Thread(target=handle_client, args=(client_socket,)).start()

# Main function to start the server
def main():
    port = 38986  # Change to the desired port number
    start_server(port)

if __name__ == "__main__":
    main()
