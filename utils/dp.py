import mysql.connector

def get_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # XAMPP default is empty unless you set one
        database="jaltal"
    )
    return connection
