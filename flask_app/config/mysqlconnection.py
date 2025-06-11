import os
from urllib.parse import urlparse
import pymysql.cursors
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the composite DATABASE_URL from your .env or Heroku config vars
DATABASE_URL = os.environ.get('DATABASE_URL')
# Example: mysql://username:password@hostname:port/databasename

# Parse the URL to extract connection details
url = urlparse(DATABASE_URL)

# Extract individual components from the parsed URL
db_host = url.hostname
db_user = url.username
db_password = url.password
db_port = url.port  # By default, MySQL uses port 3306 if not provided
db_name = url.path.lstrip('/')  # Remove the leading '/' from the path

class MySQLConnection:
    def __init__(self, db):
        """
        If you pass in 'db', it can override the one in the URL.
        Otherwise, it will use the database name from your DATABASE_URL.
        """
        self.connection = pymysql.connect(
            host=db_host,            # from DATABASE_URL
            user=db_user,            # from DATABASE_URL
            password=db_password,    # from DATABASE_URL
            db=db if db else db_name, # use provided db or default db name
            port=db_port,            # from DATABASE_URL
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=False
        )

    def query_db(self, query: str, data: dict = None):
        with self.connection.cursor() as cursor:
            try:
                # Format the query with the given data
                formatted_query = cursor.mogrify(query, data)
                print("Running Query:", formatted_query)

                cursor.execute(query)
                
                # INSERT operations: commit and return the new record ID
                if query.strip().lower().startswith("insert"):
                    self.connection.commit()
                    return cursor.lastrowid
                # SELECT operations: return fetched results
                elif query.strip().lower().startswith("select"):
                    result = cursor.fetchall()
                    return result
                # UPDATE or DELETE operations
                else:
                    self.connection.commit()
            except Exception as e:
                print("Something went wrong:", e)
                return False
            finally:
                self.connection.close()

def connectToMySQL(db=None):
    """
    Returns an instance of MySQLConnection.
    If no database name is provided (db is None), it will use the one parsed from DATABASE_URL.
    """
    return MySQLConnection(db)
