# login_page.py
import sqlite3
from PyQt5.QtWidgets import *


def setup_login_page(stack, update_home_page):
    page = QWidget()
    page.setWindowTitle("Login")

    group_box = QGroupBox()
    group_box.setGeometry(250, 170, 280, 150)  # Set the size of the container
    group_box.setStyleSheet("""
    QGroupBox {
        background-color: rgba(255, 255, 255, 0);  /* Semi-transparent white */
        border: none;
    }
    QLineEdit {
        background-color: transparent;
        border: 1px solid #8ECAE6;
        margin-top: 10px;
    }
""")
    group_box.setParent(page)
    layout = QFormLayout(group_box)

    global username
    username = QLineEdit()
    global password
    password = QLineEdit()
    password.setEchoMode(QLineEdit.Password)
    btn_login = QPushButton('Log In')
    btn_login.setGeometry(365, 300, 120, 40)
    btn_login.setParent(page)
    btn_login.clicked.connect(lambda: attempt_login(
        username.text(), password.text(), stack, update_home_page))
    btn_login.setObjectName("login")

    btn_home = QPushButton("Home")
    btn_home.setGeometry(30, 30, 100, 40)
    btn_home.setParent(page)
    btn_home.clicked.connect(lambda: stack.setCurrentIndex(0))
    layout.addRow('Username ', username)
    layout.addRow('Password ', password)

    return page


def attempt_login(username, password, stack, update_home_page):
    # Connecting to the database
    conn = sqlite3.connect('Python/project/database/airline.db')
    cursor = conn.cursor()

    # Checking user information
    try:
        cursor.execute(
            'SELECT * FROM User WHERE Username=? AND Password=?', (username, password))
        global user
        user = cursor.fetchone()
        if user:
            update_home_page(user)
        else:
            show_message("Error", "Invalid Username or Password ")
            return
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
