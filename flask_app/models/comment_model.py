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
        
  

    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO comments (content, user_id, blog_post_id, parent_comment_id)
        VALUES (%(content)s, %(user_id)s, %(blog_post_id)s, %(parent_comment_id)s);
        """
        return connectToMySQL("project").query_db(query, data)



    @classmethod
    def get_by_post(cls, data):
        query = "SELECT * FROM comments WHERE blog_post_id = %(blog_post_id)s ORDER BY created_at ASC;"
        results = connectToMySQL('project').query_db(query, data)

        if not results:  
            return []  # Ensures an empty list instead of None
        
        comments = [cls(row) for row in results]  # List comprehension for cleaner code

        return comments
    
    ##return a comment
    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO comments (content, user_id, blog_post_id)
        VALUES (%(content)s, %(user_id)s, %(blog_post_id)s);
        """
        return connectToMySQL('project').query_db(query, data)  # Returns inserted ID
    
    ## handle no response
    @classmethod
    def get_by_post(cls, data):
        query = "SELECT * FROM comments WHERE blog_post_id = %(blog_post_id)s ORDER BY created_at ASC;"
        results = connectToMySQL('project').query_db(query, data)

        if not results:
            return []  # Prevents returning None

        return [cls(row) for row in results]  # Uses list comprehension for cleaner code

    


    


