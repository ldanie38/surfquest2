import pymysql.cursors

db = 'project'

class MySQLConnection:
    def __init__(self, db):
        # You can eventually update these credentials to be read from environment variables
        self.connection = pymysql.connect(
            host='localhost',
            user='root',
            password='Stanislav24',
            db=db,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=False
        )

    def query_db(self, query: str, data: dict = None):
        with self.connection.cursor() as cursor:
            try:
                # This formats the query with the data provided
                formatted_query = cursor.mogrify(query, data)
                print("Running Query:", formatted_query)
                # Pass both query and data to execute for proper substitution.
                cursor.execute(query, data)
                # If it's an INSERT operation, return the new record's id
                if query.strip().lower().startswith("insert"):
                    self.connection.commit()
                    return cursor.lastrowid
                # For SELECT operations, return all fetched data
                elif query.strip().lower().startswith("select"):
                    result = cursor.fetchall()
                    return result
                # For UPDATE and DELETE operations
                else:
                    self.connection.commit()
            except Exception as e:
                print("Something went wrong:", e)
                return False
            finally:
                self.connection.close()

def connectToMySQL(db):
    return MySQLConnection(db)
