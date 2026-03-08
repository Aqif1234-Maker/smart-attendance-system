# config.example.py
# Copy this file to config.py and fill in your MySQL credentials

import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="YOUR_PASSWORD_HERE",
            database="attendance_db"
        )
        return connection
    except Error as e:
        print(f"Database Connection Error: {e}")
        return None