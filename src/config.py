from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

REDIS_HOST=os.environ.get("REDIS_HOST", "127.0.0.1")
REDIS_PORT=os.environ.get("REDIS_PORT", "6379")
WEB_APP_HOST=os.environ.get("WEB_APP_HOST", "127.0.0.1")
WEB_APP_PORT=os.environ.get("WEB_APP_PORT", "8000")
API_APP_HOST=os.environ.get("API_APP_HOST", "127.0.0.1")
API_APP_PORT=os.environ.get("API_APP_PORT", "8000")
API_APP_PATH=os.environ.get("API_APP_PATH", "/api")
HTTP_HTTPS_PROT=os.environ.get("HTTP_HTTPS_PROT", default='http')
WS_WSS_PROT=os.environ.get("WS_WSS_PROT", default='ws')

DB_HOST_TEST = os.environ.get("DB_HOST_TEST")
DB_PORT_TEST = os.environ.get("DB_PORT_TEST")
DB_NAME_TEST = os.environ.get("DB_NAME_TEST")
DB_USER_TEST = os.environ.get("DB_USER_TEST")
DB_PASS_TEST = os.environ.get("DB_PASS_TEST")

SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")
SMTP_USER = os.environ.get("SMTP_USER")


SECRET_AUTH_COOKIE = os.environ.get("SECRET_AUTH_COOKIE")
SECRET_AUTH_USER_MANAGER = os.environ.get("SECRET_AUTH_USER_MANAGER")

OAUTH2_SECRET = os.environ.get("OAUTH2_SECRET")