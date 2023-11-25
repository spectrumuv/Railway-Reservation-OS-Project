# Railway Reservation System


The Railway Reservation System is a Python-based client-server application that manages train reservations for users. This system allows users to register, log in, book tickets, cancel booked tickets, and manage their profiles. Administrators can register trains, delete trains, and perform other administrative tasks.

# Features


The Railway Reservation System is a Python-based client-server application that manages train reservations for users. This system allows users to register, log in, book tickets, cancel booked tickets, and manage their profiles. Administrators can register trains, delete trains, and perform other administrative tasks.

# Features

User Registration and Authentication: Users can create accounts by registering their details and authenticate themselves to access the system.

Train Registration and Deletion: Administrators can add new trains to the system and delete existing train records.

Ticket Booking and Cancellation: Users can search for available trains, book tickets, and cancel booked tickets if necessary.

Profile Management: Users can view and update their profile information, including age, mobile number, and full name.


# Files

The project consists of the following main files:

server.py: Implements the server-side functionality using sockets to handle client requests concurrently.

client.py: Represents the client-side code to interact with the server for user actions.

users.txt: Stores user details such as username, password, age, mobile number, and full name.

trains.txt: Contains information about registered trains, including train number, hours taken, destination station, boarding station, and available seats.

booking.txt: Stores booking details, including train number, booked seat number, and username.

README.md: This file, containing information about the project.


# Files
The project consists of the following main files:

server.py: Implements the server-side functionality using sockets to handle client requests concurrently.

client.py: Represents the client-side code to interact with the server for user actions.

users.txt: Stores user details such as username, password, age, mobile number, and full name.

trains.txt: Contains information about registered trains, including train number, hours taken, destination station, boarding station, and available seats.

booking.txt: Stores booking details, including train number, booked seat number, and username.

README.md: This file, containing information about the project.
# Setup Instructions

Clone the Repository:

git clone https://github.com/username/Railway-Reservation-System.git

Start the Server:

Run the server script using Python:

python server.py

Run the Client:

Execute the client script to interact with the server:

python client.py



# Usage
Upon running the client script, users can select different options from the menu, such as Admin Mode, User Mode, Registration, Login, Ticket Booking, etc., to perform specific actions as per the system's functionalities.
