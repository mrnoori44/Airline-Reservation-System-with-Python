import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtGui

from login_page import setup_login_page
import login_page
from signup_page import setup_signup_page
from search_flight_page import setup_search_flights_page
from user_profile_page import setup_user_profile_page
from passenger_info_page import setup_passenger_info_page


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Airline Reservation System')
        self.setFixedSize(850, 650)

        self.stack = QStackedWidget(self)
        self.setCentralWidget(self.stack)

        self.setAutoFillBackground(True)
        p = self.palette()
        p.setBrush(self.backgroundRole(), QtGui.QBrush(
            QtGui.QPixmap('Python/project/airplane.jpg')))
        self.setPalette(p)

        self.user_logged_in = False  # Variable to track user login status
        self.user_first_name = None  # Variable to store the user's first name
        self.selected_flight = None

        self.init_ui()

    def init_ui(self):
        self.stack.addWidget(self.create_home_page())
        self.stack.addWidget(setup_login_page(
            self.stack, self.update_home_page))
        self.stack.addWidget(setup_signup_page(self.stack))
        self.stack.addWidget(setup_search_flights_page(self.stack))
        self.stack.addWidget(setup_passenger_info_page(
            self.stack, self.selected_flight))

        self.show_home_page()

    def create_home_page(self):
        page = QWidget()

        if not self.user_logged_in:
            title_lbl = QLabel("Welcome to the Airline Reservation System")
            title_lbl.setObjectName("title")
            title_lbl.move(50, 50)
            title_lbl.setParent(page)

            subtitle_lbl = QLabel(
                "Please Login to your Account or Sign up a new one to access our services")
            subtitle_lbl.setObjectName("subtitle")
            subtitle_lbl.move(50, 150)
            subtitle_lbl.setParent(page)

            btn_login = QPushButton('Login')
            btn_login.setGeometry(40, 250, 100, 35)

            btn_login.clicked.connect(
                lambda: self.stack.setCurrentIndex(1))  # Go to login page
            btn_login.setParent(page)

            btn_signup = QPushButton('Sign Up')
            btn_signup.setGeometry(150, 250, 100, 35)
            btn_signup.setObjectName("signup")
            btn_signup.clicked.connect(
                lambda: self.stack.setCurrentIndex(2))
            btn_signup.setParent(page)  # Go to sign up page

        else:
            lbl_user_name = QLabel(f"Welcome, {self.user_first_name}!")
            lbl_user_name.setObjectName("username")
            lbl_user_name.move(50, 80)
            lbl_user_name.setParent(page)

            description_lbl = QLabel(
                "You can now search for flight tickets to all around the world\nAlso don't forget to check your profile to see your reserved tickets")
            description_lbl.setObjectName("description")
            description_lbl.move(50, 140)
            description_lbl.setParent(page)

            btn_search_flights = QPushButton('Search Flights')
            btn_search_flights.setGeometry(40, 250, 130, 50)
            btn_search_flights.setParent(page)
            btn_search_flights.clicked.connect(
                lambda: self.stack.setCurrentIndex(3))  # Go to search flights page

            btn_user_profile = QPushButton('User Profile')
            btn_user_profile.setGeometry(180, 250, 110, 50)
            btn_user_profile.setParent(page)
            btn_user_profile.clicked.connect(
                lambda: self.switch_to_profile(login_page.user))  # Go to user profile page

        return page

    def switch_to_profile(self, user):
        self.user_profile_page = setup_user_profile_page(
            self.stack, user, self.update_home_page)
        self.stack.addWidget(self.user_profile_page)
        self.stack.setCurrentWidget(self.user_profile_page)

    def show_home_page(self):
        self.stack.setCurrentIndex(0)

    def update_home_page(self, user=None):
        self.user_logged_in = True if user else False
        self.user_first_name = user[4] if user else None
        self.stack.removeWidget(self.stack.widget(0))
        self.stack.insertWidget(0, self.create_home_page())
        self.stack.setCurrentIndex(0)


if __name__ == '__main__':
    QLocale.setDefault(QLocale(QLocale.English, QLocale.UnitedStates))
    app = QApplication(sys.argv)
    # Set the style for the whole application

    app.setStyleSheet("""
        QWidget {

            color: #e1e5f2;
            font-size:16px;
            font-family: 'Rubik';
            font-weight: bold;
        }

        #title, #username, #profile {
            color:#fefae0; 
            font-size: 30px; 
            font-weight:bold;
        }
        #subtitle, #description{
            color:#fefae0;
            font-size: 16px; 
            font-weight: bold;
        }
        
        

        
        QPushButton {
            background-color: #fefae0;
            border: none;
            border-radius: 4px;
            color: #001a23;
            font-weight: bold;
        
            
        }
        QPushButton:hover {
            background-color:#e9edc9;
            border: 1px solid #d6ccc2;
        
        }

        #signup, #login, #register, #search, #submit {
            background-color:#023047;
            color:#fefae0; 
            border: none;
        }
        #reserve {
            background-color: #098E59; 
            color:#AEE3CB; 
            border: none; 
            border-radius: none;
            padding: 0 10px;
        }
        #cancel {
            background-color: #ef233c;
            color:#fefae0;
            border: none;
            border-radius: none;
            padding: 0 10px;
        }

        #signup:hover {
            background-color: #01161e;
            border: 1px solid #124559;
        }
        #login:hover {
            background-color: #01161e;
            border: 1px solid #124559;
        }
        #register:hover{
            background-color: #01161e;
            border: 1px solid #124559;
        }
        #search:hover{
            background-color: #01161e;
            border: 1px solid #124559;
        }
        #reserve:hover{
            background-color: #055535;
            border: 1px solid #AEFADB;
        }
        #submit:hover{
            background-color: #01161e;
            border: 1px solid #124559;
        }
        #cancel:hover{
            background-color: #d80032;
            border: 1px solid #edf2f4;
        }
    
        QLineEdit, QComboBox {
            background-color: #decdf5;
            color: #001a23;
        }

        QCalendarWidget QWidget {
        color: #023047;
        background-color: #fdf0d5;
    }
        QCalendarWidget QAbstractItemView {
            selection-background-color: #669bbc;
            selection-color: #edf3fe;
    }
        QCalendarWidget QHeaderView::section {
            background-color: #6a6ea9;
            color: #fff;
            padding: 5px;
            border: 1px solid #6a6ea9;
            margin: 1px;
    }
        QCalendarWidget QToolButton {
            color: #333;
            background-color: #dcdcdc;
            border: none;
    }
        QTableWidget {
            background-color: #AEE3CB;
            color: #021C12;
            font-size: 13px;
            font-weight: bold;
        }
        QHeaderView::section {
        background-color: #AEE3CB;
        color: #021C12;
        padding: 2px;
        border-right: 1px solid #AEE3CB;
        font-size: 12px;
        font-weight: bold;
    }
        QMessageBox {
        background-color: #e6e8e6;
        color: #011627;
        font-size: 15px;
    }

        QMessageBox QLabel{
            color:#011627;
        }
    

    /* Style the QPushButton inside the QMessageBox */
        QMessageBox QPushButton {
            background-color: #2b2d42;
            color: #e6e8e6;
            border-radius: 5px;
            padding:7px;
            border: none;
    }

    /* Style the QPushButton when it's hovered over */
        QMessageBox QPushButton:hover {
            background-color: #011627;

    }
    """)

    ex = App()
    ex.show()  # Make sure to call show() on the main window
    sys.exit(app.exec_())
