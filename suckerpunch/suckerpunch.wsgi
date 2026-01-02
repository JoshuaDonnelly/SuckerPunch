import sys
import os

# Ensure project path
sys.path.insert(0, "/var/www/suckerpunch")

# Load environment variables BEFORE importing Flask
from dotenv import load_dotenv
load_dotenv("/var/www/suckerpunch/.env")

from suckerpunch import app as application

