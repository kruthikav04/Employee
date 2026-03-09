import mysql.connector

def get_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="appuser",
        password="AppUser@123",
        database="airowire_db"
    )
    return connection
