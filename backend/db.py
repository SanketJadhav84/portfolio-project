import os
import time
import mysql.connector

def get_connection():
    retries = 10
    while retries > 0:
        try:
            conn = mysql.connector.connect(
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_NAME")
            )
            print("Connected to MySQL successfully")
            return conn
        except mysql.connector.Error as e:
            print(f"MySQL not ready, retrying... ({e})")
            retries -= 1
            time.sleep(5)
    raise Exception("Could not connect to MySQL after multiple retries")

db = get_connection()
cursor = db.cursor()