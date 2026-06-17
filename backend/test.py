import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="sanket@0000",
    database="portfolio"
)

print("Connected Successfully")