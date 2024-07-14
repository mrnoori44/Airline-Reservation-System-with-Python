# user_profile_page.py
from PyQt5.QtWidgets import *
import login_page
import sqlite3


def setup_user_profile_page(stack, user, update_home_page):
    page = QWidget()
    page.setWindowTitle("User Profile")
    group_box = QGroupBox()
    group_box.setGeometry(200, 100, 450, 300)
    group_box.setParent(page)
    group_box.setStyleSheet(
        """
        QGroupBox {
        background-color: rgba(255, 255, 255, 0);  
        border: none;
    }
        """
    )

    layout = QVBoxLayout(group_box)

    label_welcome = QLabel(f'Welcome, {user[4]} {user[5]}')
    label_welcome.setObjectName("profile")

    btn_reserved_flights = QPushButton('Reserved Flights')
    btn_reserved_flights.clicked.connect(
        lambda: search_reserved_flights(user))

    btn_home = QPushButton("Home")
    btn_home.clicked.connect(lambda: stack.setCurrentIndex(0))

    btn_logout = QPushButton('Logout')
    btn_logout.setStyleSheet("background-color: #c81d25; color: #ffffff;")
    btn_logout.clicked.connect(lambda: logout(
        update_home_page, login_page.username, login_page.password))

    layout.addWidget(label_welcome)
    layout.addWidget(btn_reserved_flights)
    layout.addWidget(btn_home)
    layout.addWidget(btn_logout)

    return page


def logout(update_home_page, username, password):
    # Clear the text of the QLineEdit widgets
    username.clear()
    password.clear()

    # Go back to home page and update login status
    update_home_page()


def search_reserved_flights(user):
    # Connect to the SQLite database
    conn = sqlite3.connect('Python/project/database/airline.db')
    c = conn.cursor()

    # Get the flights reserved by the user
    try:
        c.execute(
            "SELECT Flight.* FROM Flight INNER JOIN Booking ON Flight.FlightID = Booking.FlightID WHERE Booking.UserID = ?", (user[0],))
        reserved_flights = c.fetchall()
        if reserved_flights:
            display_reserved_flights(user, reserved_flights)
        else:
            show_message("Info", "No Flights were found")
            return
    except sqlite3.Error as e:
        show_message('Error', str(e))
    finally:
        c.close()


def display_reserved_flights(user, reserved_flights):
    # Create a table widget to display the flights
    global table
    table = QTableWidget(len(reserved_flights), len(reserved_flights[0]))

    # Set the column headers
    # Adjust this based on your actual data
    table.setHorizontalHeaderLabels(["Departure", "Arrival", "Dep.Time", "Arr.Time",
                                    "Dep.Airport", "Arr.Airport", "Duration", "AvailableSeats", "Airline", "Price", "Flight Date"])

    # Add the flight data to the table
    for i, flight in enumerate(reserved_flights):

        table.setItem(i, 0, QTableWidgetItem(str(flight[2])))
        table.setItem(i, 1, QTableWidgetItem(str(flight[3])))
        table.setItem(i, 2, QTableWidgetItem(str(flight[6])))
        table.setItem(i, 3, QTableWidgetItem(str(flight[7])))
        table.setItem(i, 4, QTableWidgetItem(str(flight[4])))
        table.setItem(i, 5, QTableWidgetItem(str(flight[5])))
        table.setItem(i, 6, QTableWidgetItem(str(flight[8])))
        table.setItem(i, 7, QTableWidgetItem(str(flight[9])))
        table.setItem(i, 8, QTableWidgetItem(str(flight[1])))
        table.setItem(i, 9, QTableWidgetItem(str(flight[10])))
        table.setItem(i, 10, QTableWidgetItem(str(flight[11])))

        # Create a 'Cancel' button for each flight
        btn_cancel = QPushButton('Cancel')
        btn_cancel.setObjectName("cancel")
        btn_cancel.clicked.connect(
            lambda checked, row=i: cancel_flight(user, reserved_flights[row]))

        # Add the 'Cancel' button to the table
        table.setCellWidget(i, table.columnCount() - 1, btn_cancel)

    table.setSelectionBehavior(QTableWidget.SelectRows)
    table.setSelectionMode(QTableWidget.SingleSelection)

    # Resize the columns and rows to fit the contents
    table.resizeColumnsToContents()
    table.resizeRowsToContents()
    table.setMinimumSize(1000, 600)
    table.setWindowTitle("Reserved Flights")

    # Show the table
    table.show()


def cancel_flight(user, flight):
    # Connect to the SQLite database
    conn = sqlite3.connect('Python/project/database/airline.db')
    c = conn.cursor()

    # Delete the booking from the Booking table
    c.execute("DELETE FROM Booking WHERE UserID = ? AND FlightID = ?",
              (user[0], flight[0]))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    table.close()

    show_message("Success", "Your Ticket has been Canceled Successfully.")
    return


def show_message(title, message):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText(message)
    msg.setWindowTitle(title)
    msg.exec_()
