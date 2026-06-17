import mysql.connector

db = mysql.connector.connect(
    host="mysql",
    user="root",
    password="root123",
    database="portfolio"
)

cursor = db.cursor()