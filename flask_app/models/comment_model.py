# flask_app/models/comment.py
from flask_app.config.mysqlconnection import connectToMySQL

class Comment:
    def __init__(self, data):
        self.id = data['id']
        self.content = data['content']
        self.user_id = data['user_id']
        self.blog_post_id = data['blog_post_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
  

    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO comments (content, user_id, blog_post_id)
        VALUES (%(content)s, %(user_id)s, %(blog_post_id)s);
        """
        return connectToMySQL('project').query_db(query, data)

    @classmethod
    def get_by_post(cls, data):
        query = "SELECT * FROM comments WHERE blog_post_id = %(blog_post_id)s ORDER BY created_at ASC;"
        results = connectToMySQL('project').query_db(query, data)
        comments = []
        for row in results:
            comments.append(cls(row))
        return comments
    


