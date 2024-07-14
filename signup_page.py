# signup_page.py
import sqlite3
import re
from PyQt5.QtWidgets import *


def setup_signup_page(stack):
    page = QWidget()
    page.setWindowTitle("Sign Up")

    group_box = QGroupBox()
    group_box.setGeometry(250, 100, 320, 290)
    group_box.setStyleSheet("""
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
    QDateEdit QCalendarWidget{
        color:#023047;
    }
    
    """)
    group_box.setParent(page)

    username = QLineEdit()
    password = QLineEdit()
    password.setEchoMode(QLineEdit.Password)
    email = QLineEdit()
    first_name = QLineEdit()
    last_name = QLineEdit()
    date_of_birth = QDateEdit()
    date_of_birth.setDisplayFormat("dd-MM-yyyy")
    date_of_birth.setCalendarPopup(True)

    btn_signup = QPushButton('Register')
    btn_signup.setGeometry(365, 400, 130, 40)
    btn_signup.setObjectName("register")
    btn_signup.setParent(page)
    btn_signup.clicked.connect(lambda: register_user(stack, username.text(), password.text(
    ), email.text(), first_name.text(), last_name.text(), date_of_birth.text()))

    btn_home = QPushButton("Home")
    btn_home.setGeometry(30, 30, 100, 40)
    btn_home.setParent(page)
    btn_home.clicked.connect(lambda: stack.setCurrentIndex(0))

    layout = QFormLayout(group_box)
    layout.addRow('Username ', username)
    layout.addRow('Password ', password)
    layout.addRow('Email ', email)
    layout.addRow('First Name ', first_name)
    layout.addRow('Last Name ', last_name)
    layout.addRow('Date of Birth ', date_of_birth)

    return page


def register_user(stack, username, password, email, first_name, last_name, date_of_birth):
    # Validating inputs
    if not all([username, password, email, first_name, last_name, date_of_birth]):
        show_message('Error', 'All fields must be filled.')
        return

    if not 4 <= len(username) <= 20:
        show_message(
            'Error', 'Username must be between 4 and 20 characters long')
        return

    if not 8 <= len(password):
        show_message("Error", "Password must be at least 8 characters")
        return

    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        show_message('Error', 'Please enter a valid email address')
        return

    if len(first_name) > 20 or len(last_name) > 20:
        show_message(
            'Error', 'First name and last name must not exceed 20 characters each.')
        return
    # Connect to the database
    conn = sqlite3.connect('../database/airlinesystem0.db')
    cursor = conn.cursor()

    # Check if the username or email already exists
    cursor.execute(
        "SELECT * FROM User WHERE Username=? OR Email=?", (username, email))
    if cursor.fetchone():
        show_message('Error', 'Username or Email already exists!')
        return

    # Insert the new user into the database
    try:
        cursor.execute("INSERT INTO User (Username, Password, Email, FirstName, LastName, DateOfBirth, RegistrationDate) VALUES (?, ?, ?, ?, ?, ?, date('now'))",
                       (username, password, email, first_name, last_name, date_of_birth))
        conn.commit()
        show_message('Success', 'You have been registered successfully!')
        stack.setCurrentIndex(0)  # Go back to home page
    except sqlite3.Error as e:
        show_message('Error', str(e))
    finally:
        conn.close()


def show_message(title, message):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText(message)
    msg.setWindowTitle(title)
    msg.exec_()
