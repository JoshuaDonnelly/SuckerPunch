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

        user_id = get_or_create_user(user_info)
        session["user_id"] = user_id

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

@app.route('/sessions')
def sessions():
    """Our Excersise sessions selector """
    return render_template("sessions.html")

@app.route('/shadow')
def shadow():
    """Our Shadow box routine page """
    data = {
        'title': request.args.get("title", "Shadowboxing Session"),
        'desc': request.args.get("desc", "A focused shadowboxing routine."),
        'duration': request.args.get("duration", "15 min"),
        'focus': request.args.get("focus", "General Fitness")
    }
    return render_template("shadow.html", **data)

from .db import get_db

def get_or_create_user(user_info):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT id FROM users WHERE google_sub = %s",
        (user_info["sub"],)
    )
    user = cursor.fetchone()

    if not user:
        cursor.execute(
            """
            INSERT INTO users (google_sub, email, name)
            VALUES (%s, %s, %s)
            """,
            (user_info["sub"], user_info["email"], user_info.get("name"))
        )
        conn.commit()
        user_id = cursor.lastrowid
    else:
        user_id = user["id"]

    cursor.close()
    conn.close()
    return user_id

@app.route("/my-sessions")
def my_sessions():
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT id, title, description, focus, minutes, created_at
        FROM shadow_sessions
        WHERE user_id = %s
        ORDER BY created_at DESC
        """,
        (session["user_id"],)
    )

    sessions = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("my_sessions.html", sessions=sessions)

@app.route("/sessions/load/<int:session_id>")
def load_session(session_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT title, description, focus, minutes
        FROM shadow_sessions
        WHERE id = %s AND user_id = %s
        """,
        (session_id, session["user_id"])
    )

    s = cursor.fetchone()

    cursor.close()
    conn.close()

    if not s:
        return "Session not found", 404

    return redirect(url_for(
        "shadow",
        title=s["title"],
        desc=s["description"],
        focus=s["focus"],
        duration=f'{s["minutes"]} min'
    ))
