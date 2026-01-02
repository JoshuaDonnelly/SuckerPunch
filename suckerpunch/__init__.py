from flask import Flask, render_template
from dotenv import load_dotenv
import os
import mysql.connector

load_dotenv("/var/www/suckerpunch/.env")

app = Flask(
    __name__,
    static_folder="static",
    static_url_path="/static"
)

# Add PubNub config to Flask app
app.config['PUBNUB_SUBSCRIBE_KEY'] = os.getenv("PUBNUB_SUB_KEY")
app.config['PUBNUB_PUBLISH_KEY'] = os.getenv("PUBNUB_PUB_KEY")

from .routes import api
app.register_blueprint(api)

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
