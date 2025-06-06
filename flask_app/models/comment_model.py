# flask_app/models/comment.py
from flask_app.config.mysqlconnection import connectToMySQL

class Comment:
    def __init__(self, data):
        self.id = data['id']
        self.content = data['content']
        self.user_id = data['user_id']
        self.blog_post_id = data['blog_post_id']
        self.parent_comment_id = data.get("parent_comment_id")
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.image_url = data.get('image_url')  # Use get() to handle when it's not provided

    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO comments (content, user_id, blog_post_id, image_url)
        VALUES (%(content)s, %(user_id)s, %(blog_post_id)s, %(image_url)s);
        """
        return connectToMySQL("project").query_db(query, data)

    @classmethod
    def get_by_post(cls, data):
        query = """
        SELECT comments.*, users.username 
        FROM comments
        JOIN users ON comments.user_id = users.id
        WHERE blog_post_id = %(blog_post_id)s
        ORDER BY comments.created_at ASC;
        """
        results = connectToMySQL('project').query_db(query, data)

        if not results:
            return []

        comments = []
        for row in results:
            comment = cls(row)
            comment.username = row['username']  # Attach username from joined query
            comments.append(comment)

        return comments
