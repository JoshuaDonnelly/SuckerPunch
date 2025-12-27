#!/usr/bin/python3
import sys
import logging
import os

logging.basicConfig(stream=sys.stderr)

project_path = "/var/www/suckerpunch"
if project_path not in sys.path:
    sys.path.insert(0, project_path)

# Optional environment defaults
os.environ.setdefault("TEST", "test")
os.environ.setdefault("FACEBOOK_APP", "your_facebook_app_id")
os.environ.setdefault("FACEBOOK_SECRET", "your_facebook_app_secret")

from suckerpunch import app as application

application.secret_key = "secret"


