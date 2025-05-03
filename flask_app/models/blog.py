from flask_app.config.mysqlconnection import connectToMySQL

class BlogPost:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.content = data['content']
        self.author = data['author']
        self.created_at = data['created_at']
        self.likes = data['likes']
        
    db='project'
    
    @classmethod
    def save(cls, data):
        query = '''INSERT INTO blog_posts (title, content, author)
                   VALUES (%(title)s, %(content)s, %(author)s);'''
        return connectToMySQL('project').query_db(query, data)

    @classmethod
    def get_all(cls):
        query = '''SELECT * FROM blog_posts ORDER BY created_at DESC;'''
        results = connectToMySQL('project').query_db(query)
        return [cls(row) for row in results] if results else []

    @classmethod
    def get_by_id(cls, data):
        query = '''SELECT * FROM blog_posts WHERE id = %(id)s;'''
        results = connectToMySQL('project').query_db(query, data)
        return cls(results[0]) if results else None
    
    @classmethod
    def increment_like(cls, post_id):
        # Increment the like count
        query = "UPDATE blog_posts SET likes = likes + 1 WHERE id = %(id)s;"
        data = {"id": post_id}
        connectToMySQL('project').query_db(query, data)
        
        # Retrieve the new like count
        query = "SELECT likes FROM blog_posts WHERE id = %(id)s;"
        result = connectToMySQL('project').query_db(query, data)
        
        if result and len(result) > 0:
            return result[0]['likes']
        return None
    
    @classmethod
    def get_total_likes(cls):
        query = "SELECT SUM(likes) AS total_likes FROM comments;"
        result = connectToMySQL('project').query_db(query)
        return result[0]['total_likes'] if result else 0
