import os
import pymysql.cursors
from urllib.parse import urlparse

class MySQLConnection:
    def __init__(self, db):
        # Retrieve database URL from environment variables or fallback
        db_url = os.getenv("JAWSDB_URL") or os.getenv("DATABASE_URL")

        if not db_url:
            raise ValueError("Database URL not found in environment variables.")

        url = urlparse(db_url)

        if not all([url.hostname, url.username, url.password, url.path]):
            raise ValueError("Invalid database URL format.")

        self.connection = pymysql.connect(
            host=url.hostname,
            port=url.port or 3306,
            user=url.username,
            password=url.password,
            db=url.path.lstrip('/'),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )

    def query_db(self, query: str, data: dict = None):
        with self.connection.cursor() as cursor:
            try:
                if data:
                    query = cursor.mogrify(query, data)

                print("Running Query:", query)
                cursor.execute(query, data if data else ())

                if query.lower().startswith(("insert", "update", "delete")):
                    self.connection.commit()
                    return cursor.lastrowid if query.lower().startswith("insert") else True
                elif query.lower().startswith("select"):
                    return cursor.fetchall()

            except pymysql.MySQLError as e:
                print("Database error:", e)
                return False
            
            finally:
                cursor.close()

    def close_connection(self):
        """Manually close the database connection."""
        self.connection.close()

def connectToMySQL(db):
    return MySQLConnection(db)
