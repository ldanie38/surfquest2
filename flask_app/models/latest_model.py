from flask_app.config.mysqlconnection import connectToMySQL
from datetime import datetime

DB = "project"

class LatestPost:
    def __init__(self, data):
        self.id          = data['id']
        self.title       = data['title']
        self.body        = data['body']
        self.image       = data.get('image')
        self.created_at  = data['created_at']
        self.updated_at  = data.get('updated_at')

    @classmethod
    def get_all(cls):
        query   = """
            SELECT *
              FROM latest_posts
          ORDER BY created_at DESC;
        """
        results = connectToMySQL(DB).query_db(query)
        if not results:
            return []
        return [cls(row) for row in results]

    @classmethod
    def get_one(cls, data):
        query   = """
            SELECT *
              FROM latest_posts
             WHERE id = %(id)s;
        """
        result = connectToMySQL(DB).query_db(query, data)
        return cls(result[0]) if result else None

    @classmethod
    def create(cls, data):
        # Ensure created_at is provided or use now
        data.setdefault('created_at', datetime.now())
        query = """
            INSERT INTO latest_posts
                (title, body, image, created_at)
            VALUES
                (%(title)s, %(body)s, %(image)s, %(created_at)s);
        """
        return connectToMySQL(DB).query_db(query, data)

    @classmethod
    def update(cls, data):
        data.setdefault('updated_at', datetime.now())
        query = """
            UPDATE latest_posts
               SET title      = %(title)s,
                   body       = %(body)s,
                   image      = %(image)s,
                   updated_at = %(updated_at)s
             WHERE id = %(id)s;
        """
        return connectToMySQL(DB).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM latest_posts WHERE id = %(id)s;"
        return connectToMySQL(DB).query_db(query, data)
