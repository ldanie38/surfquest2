import os
import pymysql
from dotenv import load_dotenv
from urllib.parse import urlparse

# Load environment variables
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback_secret")  # Security token
    DEBUG = os.getenv("DEBUG", False)  # Debug mode setting

    # Parse the DATABASE_URL for JAWSDB configuration
    DATABASE_URL = os.getenv("JAWSDB_URL")

    if DATABASE_URL:
        parsed_url = urlparse(DATABASE_URL)
        DB_HOST = parsed_url.hostname
        DB_USERNAME = parsed_url.username
        DB_PASSWORD = parsed_url.password
        DB_NAME = parsed_url.path[1:]  # Remove the leading "/"

        # Create the MySQL connection
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USERNAME,
            password=DB_PASSWORD,
            database=DB_NAME,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=False,
        )
    else:
        print("Error: DATABASE_URL is missing. Make sure it's set in your environment variables.")
