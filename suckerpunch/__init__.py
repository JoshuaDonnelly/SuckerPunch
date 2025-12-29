from flask import Flask, render_template
from dotenv import load_dotenv
import os
import mysql.connector

app = Flask(__name__)

load_dotenv('/var/www/suckerpunch/.env')

@app.route("/")
def index():
    return render_template("index.html")

# Testing DB
def get_db():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )

conn = mysql.connector.connect(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME')
)

print(conn.is_connected())
conn.close()