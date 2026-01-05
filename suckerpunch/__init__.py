from flask import Flask, render_template, redirect, url_for, session, request
from dotenv import load_dotenv 
from authlib.integrations.flask_client import OAuth
import os
import mysql.connector
import logging
import secrets

load_dotenv("/var/www/suckerpunch/.env")

app = Flask(
    __name__,
    static_folder="static",
    static_url_path="/static"
)
app.debug = True
app.secret_key = os.getenv("FLASK_SECRET_KEY")

app.config.update(
    SESSION_COOKIE_SECURE=True,    
    SESSION_COOKIE_HTTPONLY=True,  
    SESSION_COOKIE_SAMESITE='Lax', 
)

# Add PubNub config to Flask app
app.config['PUBNUB_SUBSCRIBE_KEY'] = os.getenv("PUBNUB_SUB_KEY")
app.config['PUBNUB_PUBLISH_KEY'] = os.getenv("PUBNUB_PUB_KEY")

from .routes import api
app.register_blueprint(api)

oauth = OAuth(app)

oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_OAUTH_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_OAUTH_CLIENT_SECRET"),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'  
    }
)

@app.route('/login')
def login():
    """Redirects the user to Google's login page."""
    session.clear()
    
    nonce = secrets.token_urlsafe(16)
    session['nonce'] = nonce
    redirect_uri = url_for('auth_callback', _external=True)

    return oauth.google.authorize_redirect(redirect_uri, nonce=nonce)

logging.basicConfig(level=logging.DEBUG)

@app.route('/login/callback')
def auth_callback():
    """Handles the response from Google after user login."""
    try:
        app.logger.debug("Auth callback triggered.")
        app.logger.debug(f"Request args received: {dict(request.args)}")

        token = oauth.google.authorize_access_token()
        app.logger.debug(f"Access token received: {token}")

        nonce = session.pop('nonce', None)
        user_info = oauth.google.parse_id_token(token, nonce=nonce)
        app.logger.debug(f"User info parsed: {user_info}")

        session['user'] = user_info
        app.logger.debug("User info stored in session successfully.")

        return redirect(url_for('index'))

    except Exception as e:
        app.logger.error(f"Error in auth_callback: {str(e)}", exc_info=True)
        return f"Authentication failed: {str(e)}", 500
    
@app.route('/logout')
def logout():
    """Clears the user session."""
    session.pop('user', None)
    return redirect(url_for('index'))

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
