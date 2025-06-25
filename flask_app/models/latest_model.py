from flask_app.config.mysqlconnection import connectToMySQL
from datetime import datetime

DB = "project"

class LatestPost:
    def __init__(self, data):
        self.id        = data['id']
        self.title     = data['title']
        self.body      = data['body']
        self.created_at= data['created_at']
        self.updated_at = data.get('updated_at') 


    @classmethod
    def get_all(cls):
        query   = "SELECT * FROM latest_posts ORDER BY created_at DESC;"
        results = connectToMySQL(DB).query_db(query)
        if not results:
            return []
        return [cls(row) for row in results]


    @classmethod
    def create(cls, data):
        query = """
          INSERT INTO latest_posts (title, body, created_at)
          VALUES (%(title)s, %(body)s, %(created_at)s);
        """
        return connectToMySQL(DB).query_db(query, data)
