# search_flights_page.py
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from passenger_info_page import setup_passenger_info_page
import sqlite3


class CustomCalendar(QCalendarWidget):
    def __init__(self, available_dates, parent=None):
        super().__init__(parent)
        self.available_dates = available_dates

        # Format for available dates
        self.format_available = QTextCharFormat()
        self.format_available.setFontWeight(QFont.Bold)
        self.format_available.setForeground(QColor('green'))
        self.format_available.setFontPointSize(12)

        # Format for unavailable dates
        self.format_unavailable = QTextCharFormat()
        self.format_unavailable.setForeground(QColor('red'))

        # Apply the text formats to the dates
        self.apply_date_formats()

    def set_available_dates(self, dates):
        self.available_dates = dates
        self.update()

    def apply_date_formats(self):
        # Set the format for all dates to red
        self.setMinimumDate(min(self.available_dates))
        self.setMaximumDate(max(self.available_dates))
        current_date = min(self.available_dates)
        while current_date <= max(self.available_dates):
            if current_date not in self.available_dates:
                self.setDateTextFormat(current_date, self.format_unavailable)
            else:
                self.setDateTextFormat(current_date, self.format_available)
            current_date = current_date.addDays(1)


class CustomDateEdit(QLineEdit):
    def __init__(self, available_dates, parent=None):
        super().__init__(parent)
        self.available_dates = available_dates

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.show_calendar()
        else:
            super().mousePressEvent(event)

    def show_calendar(self):
        self.dialog = QDialog(self)
        self.calendar = CustomCalendar(self.available_dates)
        self.calendar.clicked.connect(self.update_date)
        layout = QVBoxLayout(self.dialog)
        layout.addWidget(self.calendar)
        self.dialog.exec_()

    def update_date(self, date):
        locale = QLocale("C")
        self.setText(locale.toString(date, 'dd/MM/yyyy'))
        self.dialog.accept()


def setup_search_flights_page(stack):
    page = QWidget()
    page.setWindowTitle("Search Flights")
    group_box = QGroupBox()
    group_box.setGeometry(250, 100, 360, 180)
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

    departure_city = QComboBox()
    arrival_city = QComboBox()

    available_dates = get_available_flight_dates()
    departure_date = CustomDateEdit(available_dates)
    departure_date.setStyleSheet("background-color: #fdf0d5;")

    # Populate the combo boxes with data from your database
    # For example, you might want to add all unique cities from the database to the combo boxes
    departure_cities = get_departure_city()
    arrival_cities = get_arrival_city()
    departure_city.addItems(departure_cities)
    arrival_city.addItems(arrival_cities)

    btn_search = QPushButton('Search')
    btn_search.setObjectName("search")
    btn_search.setGeometry(400, 300, 110, 40)
    btn_search.setParent(page)
    btn_search.clicked.connect(lambda: search_flights(stack, departure_city.currentText(
    ), arrival_city.currentText(), departure_date.text()))

    btn_home = QPushButton("Home")
    btn_home.setGeometry(30, 30, 100, 40)
    btn_home.setParent(page)
    btn_home.clicked.connect(lambda: stack.setCurrentIndex(0))

    layout.addRow('From ', departure_city)
    layout.addRow('To ', arrival_city)
    layout.addRow('Date ', departure_date)

    return page


def search_flights(stack, departure_city, arrival_city, departure_date):
    # Connect to the database
    conn = sqlite3.connect('Python/project/database/airline.db')
    cursor = conn.cursor()

    # Query the database for flights that match the user's criteria
    cursor.execute("SELECT * FROM Flight WHERE DepartureCity=? AND ArrivalCity=? AND FlightDate=?",
                   (departure_city, arrival_city, departure_date))

    flights = cursor.fetchall()
    if flights:
        # Display the search results
        # This is a placeholder, you'll need to implement a way to display these results in your UI
        display_flights(stack, flights)
    else:
        # Show a message that no flights were found
        show_message("Not found", "No flights were found based on your input")

    conn.close()


def get_available_flight_dates():
    conn = sqlite3.connect('Python/project/database/airline.db')
    cursor = conn.cursor()

    # Query for distinct departure dates
    cursor.execute("SELECT DISTINCT FlightDate FROM Flight")
    date_records = cursor.fetchall()

    # Convert the date strings to QDate objects
    available_dates = []
    for date_record in date_records:
        # Assuming the date is stored in the format 'YYYY-MM-DD HH:MM:SS'
        date_str = date_record[0].split(' ')[0]  # Extract just the date part
        year, month, day = map(int, date_str.split('/'))
        available_dates.append(QDate(day, month, year))

    conn.close()
    return available_dates


def get_departure_city():
    conn = sqlite3.connect('Python/project/database/airline.db')
    cursor = conn.cursor()

    cursor.execute('SELECT DISTINCT DepartureCity FROM Flight')
    records = cursor.fetchall()
    conn.close()

    departure_cities = []
    for record in records:
        departure_cities.append(record[0])

    return departure_cities


def get_arrival_city():
    conn = sqlite3.connect('Python/project/database/airline.db')
    cursor = conn.cursor()

    cursor.execute('SELECT DISTINCT ArrivalCity FROM Flight')
    records = cursor.fetchall()
    conn.close()
    arrival_cities = []
    for record in records:
        arrival_cities.append(record[0])

    return arrival_cities


def display_flights(stack, flights):
    # Create a table widget with the appropriate number of rows and columns
    global table
    table = QTableWidget(len(flights), len(flights[0]))

    # Set the column headers
    # Adjust this based on your actual data
    table.setHorizontalHeaderLabels(
        ["Departure", "Arrival", "Dep.Time", "Arr.Time", "Dep.Airport", "Arr.Airport", "Duration", "AvailableSeats", "Airline", "Price"])

    # Add the flight data to the table
    for i, flight in enumerate(flights):

        table.setItem(i, 0, QTableWidgetItem(str(flight[2])))
        table.setItem(i, 1, QTableWidgetItem(str(flight[3])))
        table.setItem(i, 2, QTableWidgetItem(str(flight[6])))
        table.setItem(i, 3, QTableWidgetItem(str(flight[7])))
        table.setItem(i, 4, QTableWidgetItem(str(flight[4])))
        table.setItem(i, 5, QTableWidgetItem(str(flight[5])))
        table.setItem(i, 6, QTableWidgetItem(str(flight[8])))
        table.setItem(i, 7, QTableWidgetItem(str(flight[9])))
        table.setItem(i, 8, QTableWidgetItem(str(flight[1])))
        table.setItem(i, 9, QTableWidgetItem(
            str("${:.2f}".format(flight[10]/100))))
        table.removeColumn(10)

        button = QPushButton("Reserve")
        button.setObjectName("reserve")
        button.clicked.connect(
            lambda checked, row=i: confirm_selection(stack, flights, row))

        # Add the button to the table
        table.setCellWidget(i, table.columnCount() - 1, button)

    table.setSelectionBehavior(QTableWidget.SelectRows)
    table.setSelectionMode(QTableWidget.SingleSelection)

    # Resize the columns and rows to fit the contents
    table.resizeColumnsToContents()
    table.resizeRowsToContents()
    table.setMinimumSize(1000, 500)
    table.setWindowTitle("Flights")

    # Show the table
    table.show()


def confirm_selection(stack, flights, row):
    selected_flight = flights[row]
    selected_flight_dic = {
        "FlightID": selected_flight[0],
        "Airline": selected_flight[1],
        "DepartureCity": selected_flight[2],
        "ArrivalCity": selected_flight[3],
        "DepartureAirport": selected_flight[4],
        "ArrivalAirport": selected_flight[5],
        "DepartureTime": selected_flight[6],
        "ArrivalTime": selected_flight[7],
        "Duration": selected_flight[8],
        "AvailableSeats": selected_flight[9],
        "Price": selected_flight[10],
        "FlightDate": selected_flight[11]

    }
    table.close()
    passenger_info_page = setup_passenger_info_page(stack, selected_flight_dic)
    stack.addWidget(passenger_info_page)
    stack.setCurrentWidget(passenger_info_page)


def show_message(title, message):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText(message)
    msg.setWindowTitle(title)
    msg.exec_()
