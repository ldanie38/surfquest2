import os
import pymysql.cursors
from urllib.parse import urlparse

db = 'project'

class MySQLConnection:
    def __init__(self, db):
        # Check if the database URL from Heroku's JAWSDB add-on is set in the environment.
        db_url = os.environ.get('JAWSDB_URL')
        if db_url:
            # Parse the URL and extract connection details.
            url = urlparse(db_url)
            connection_config = {
                'host': url.hostname,
                'user': url.username,
                'password': url.password,
                'db': url.path.lstrip('/'),
                'charset': 'utf8mb4',
                'cursorclass': pymysql.cursors.DictCursor,
                'autocommit': False,
                'port': url.port or 3306
            }
            print("Using JAWSDB_URL from environment.")
        else:
            # Fallback to your local development settings.
            connection_config = {
                'host': 'localhost',
                'user': 'root',
                'password': 'Stanislav24',
                'db': db,
                'charset': 'utf8mb4',
                'cursorclass': pymysql.cursors.DictCursor,
                'autocommit': False
            }
            print("Using local DB credentials.")

        try:
            self.connection = pymysql.connect(**connection_config)
        except Exception as e:
            print("Error connecting to the database:", e)
            raise

    def query_db(self, query: str, data: dict = None):
        with self.connection.cursor() as cursor:
            try:
                # Format the query with the provided data for debugging.
                formatted_query = cursor.mogrify(query, data)
                print("Running Query:", formatted_query)
                cursor.execute(query, data)
                # Handle INSERT, SELECT, UPDATE, or DELETE accordingly.
                if query.strip().lower().startswith("insert"):
                    self.connection.commit()
                    return cursor.lastrowid
                elif query.strip().lower().startswith("select"):
                    result = cursor.fetchall()
                    return result
                else:
                    self.connection.commit()
            except Exception as e:
                print("Something went wrong:", e)
                return False
            finally:
                self.connection.close()

def connectToMySQL(db):
    return MySQLConnection(db)

