from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import login_page
import random
from datetime import datetime
import sqlite3


def setup_confirmation_page(stack, passenger_info, flight_info):
    page = QWidget()
    page.setWindowTitle("Confirmation")
    group_box = QGroupBox()
    group_box.setGeometry(50, 150, 750, 200)
    group_box.setParent(page)
    group_box.setStyleSheet("""
        QGroupBox {
        background-color: rgba(255, 255, 255, 0);  
        border: none;
    }
        QLabel {
            color: #023047;
            margin-bottom: 10px;
        }

    """
                            )
    layout = QVBoxLayout(group_box)

    title_lbl = QLabel("Please check your Flight Ticket Information!")
    title_lbl.move(50, 90)
    title_lbl.setParent(page)

    # Display the selected flight and passenger information
    lbl_flight_info = QLabel(
        f"{flight_info['DepartureCity']} ==> {flight_info['ArrivalCity']} | Airline: {flight_info['Airline']} \nDeparture Time:{flight_info['DepartureTime']} |  Arrival Time: {flight_info['ArrivalTime']} | Flight Date: {flight_info['FlightDate']}")
    lbl_passenger_info = QLabel(
        f"Passenger Name: {passenger_info['FirstName']} {passenger_info['LastName']} | Passport Number: {passenger_info['PassportNumber']} \n Nationality: {passenger_info['Nationality']} | DateOfBirth:{passenger_info['DateOfBirth']}")
    layout.addWidget(lbl_flight_info)
    layout.addWidget(lbl_passenger_info)

    btn_confirm = QPushButton('Confirm')
    btn_confirm.setGeometry(50, 400, 110, 40)
    btn_confirm.setParent(page)
    btn_confirm.clicked.connect(lambda: confirm_booking(
        stack, flight_info, passenger_info, login_page.user))

    # Create the 'Edit' button
    btn_edit = QPushButton('Edit')
    btn_edit.setGeometry(170, 400, 90, 40)
    btn_edit.setParent(page)
    # Go back to the passenger information page
    btn_edit.clicked.connect(lambda: switch_to_passenger_info(stack))

    btn_home = QPushButton("Home")
    btn_home.clicked.connect(lambda: stack.setCurrentIndex(0))
    btn_home.setGeometry(30, 30, 100, 40)
    btn_home.setParent(page)

    return page


def confirm_booking(stack, flight, passenger, user):
    # Connect to the SQLite database
    conn = sqlite3.connect('Python/project/database/airline.db')
    c = conn.cursor()

    # Generate a random seat number between 1 and 50
    seat_number = random.randint(1, 50)

    # Insert the booking information into the Booking table
    try:
        c.execute("INSERT INTO Booking (FlightID, PassengerID, UserID, BookingDate, TravelDate, SeatNumber, Status) VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (flight['FlightID'], passenger['PassengerID'], user[0], datetime.now().strftime('%Y-%m-%d'), flight['FlightDate'], str(seat_number), 'Reserved'))
        show_message('Success', "Your flight has been reserved successfully")
    # Commit the changes and close the connection
        conn.commit()
    except sqlite3.Error as e:
        show_message("Error", str(e))
    finally:
        conn.close()

    stack.setCurrentIndex(0)


def switch_to_passenger_info(stack):
    stack.setCurrentIndex(4)


def show_message(title, message):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText(message)
    msg.setWindowTitle(title)
    msg.exec_()
