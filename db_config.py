import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="aj",
        password="123",
        database="music_db"
    )