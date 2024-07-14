from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from countries import countries
from booking_confirmation_page import setup_confirmation_page
import sqlite3
import re


def setup_passenger_info_page(stack, selected_flight_dic):
    page = QWidget()
    page.setWindowTitle("Passenger Information")

    group_box = QGroupBox()
    group_box.setGeometry(250, 100, 400, 400)
    group_box.setStyleSheet(
        """
    QGroupBox {
        background-color: rgba(255, 255, 255, 0);  
        border: none;
    }
    QLineEdit, QDateEdit{
        background-color: transparent;
        border: 1px solid #8ECAE6;
        margin-top: 5px;
        color: #023047;
    }
    QComboBox {
        background-color: rgba(255, 255, 255, 0.1);
        border: 1px solid  #8ECAE6;
        
    }
    QComboBox QAbstractItemView {
        border: 1px solid #b8c0ff;
        selection-background-color: #669bbc;
        color: #003566;

    }
    QComboBox QAbstractItemView::item {
        height: 20px;
        background-color: #fdf0d5;
    }
    QComboBox QAbstractItemView::item:selected {
        background-color: #669bbc;

    }
    
    
    """
    )
    group_box.setParent(page)
    layout = QFormLayout(group_box)

    first_name = QLineEdit()
    last_name = QLineEdit()
    date_of_birth = QDateEdit()
    date_of_birth.setDisplayFormat("dd-MM-yyyy")
    date_of_birth.setCalendarPopup(True)
    passport_number = QLineEdit()

    nationality = QComboBox()
    for country in countries:
        nationality.addItem(country)

    email = QLineEdit()
    phone_number = QLineEdit()

    btn_register = QPushButton("Submit")
    btn_register.setGeometry(365, 420, 100, 40)
    btn_register.setObjectName('submit')
    btn_register.setParent(page)
    btn_register.clicked.connect(lambda: register_passenger(stack, first_name.text(), last_name.text(
    ), date_of_birth.text(), passport_number.text(), nationality.currentText(), email.text(), phone_number.text(), selected_flight_dic))

    btn_back = QPushButton("Back")
    btn_back.setGeometry(30, 30, 80, 40)
    btn_back.setParent(page)
    btn_back.clicked.connect(lambda: stack.setCurrentIndex(3))

    btn_home = QPushButton("Home")
    btn_home.setGeometry(120, 30, 100, 40)
    btn_home.setParent(page)
    btn_home.clicked.connect(lambda: stack.setCurrentIndex(0))

    layout.addRow("First Name ", first_name)
    layout.addRow("Last Name ", last_name)
    layout.addRow("Date Of Birth ", date_of_birth)
    layout.addRow("Passport Number ", passport_number)
    layout.addRow("Nationality ", nationality)
    layout.addRow("Email ", email)
    layout.addRow("Phone Number ", phone_number)

    return page


def register_passenger(stack, first_name, last_name, date_of_birth, passport_number, nationality, email, phone_number, selected_flight_dic):
    if not all([first_name, last_name, date_of_birth, passport_number, nationality, email, phone_number]):
        show_message('Error', 'All fields must be filled.')
        return

    if not (4 <= len(first_name) <= 25):
        show_message(
            'Error', "First name must be between 4 and 25 characters.")
        return
    if not (4 <= len(last_name) <= 25):
        show_message('Error', "Last name must be between 4 and 25 characters.")
        return
    if not re.match(r'^[A-Z][0-9]{7,10}$', passport_number):
        show_message("Error", "Please enter a valid Passport number.")
        return
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        show_message("Error", "Please enter a valid email.")
        return
    if not re.match(r'^\d{11}$', phone_number):
        show_message('Error', "Please enter a valid phone number.")
        return

    # Connect to the SQLite database
    conn = sqlite3.connect('Python/project/database/airline.db')
    c = conn.cursor()

    # Insert the passenger information into the Passenger table
    try:

        c.execute("INSERT INTO Passenger (FirstName, LastName, DateOfBirth, PassportNumber, Nationality, Email, PhoneNumber) VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (first_name, last_name, date_of_birth, passport_number, nationality, email, phone_number))
        conn.commit()

    except sqlite3.Error as e:
        show_message('Error', str(e))
    finally:
        conn.close()

    passenger_info = {
        "PassengerID": c.lastrowid,
        "FirstName": first_name,
        "LastName": last_name,
        "DateOfBirth": date_of_birth,
        "PassportNumber": passport_number,
        "Nationality": nationality,
        "Email": email,
        "PhoneNumber": phone_number
    }
    flight_info = selected_flight_dic

    confirmation_page = setup_confirmation_page(
        stack, passenger_info, flight_info)
    stack.addWidget(confirmation_page)
    stack.setCurrentWidget(confirmation_page)


def show_message(title, message):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText(message)
    msg.setWindowTitle(title)
    msg.exec_()
