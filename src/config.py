from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")
SMTP_USER = os.environ.get("SMTP_USER")


SECRET_AUTH_COOKIE = os.environ.get("SECRET_AUTH_COOKIE")
SECRET_AUTH_USER_MANAGER = os.environ.get("SECRET_AUTH_USER_MANAGER")
