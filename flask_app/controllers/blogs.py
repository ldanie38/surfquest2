from flask import render_template, request, redirect, session, flash, jsonify
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_app.models.blog import BlogPost
from flask_app.models.user_model import User
from flask_app.models.comment_model import Comment
from datetime import datetime



@app.route('/blog')
def blog():
    """Display all blog posts with likes, comments, and logged-in user."""
    
    posts = BlogPost.get_all()  # Fetch all blog posts
    total_likes = BlogPost.get_total_likes()  # Fetch total likes

    # Dictionary to store comments for each blog post
    post_comments = {}

    for post in posts:
        # Convert user ID to username for display
        user = User.get_by_id({"id": post.author})
        post.author_username = user.username if user else "Unknown"

        # Fetch comments for each blog post
        post_comments[post.id] = Comment.get_by_post({"blog_post_id": post.id}) or []  # Ensures list, not None

    # Retrieve logged-in user's username from session
    username = session.get("username", None)

    return render_template('blog.html', posts=posts, username=username, total_likes=total_likes, post_comments=post_comments)


@app.route('/blog/new')
def new_blog():
    """Show the form to create a new blog post."""
    return render_template('index.html')

@app.route('/blog/create')
def prevent_get():
    """Redirect if someone tries to access /blog/create via GET."""
    flash("Invalid request method.")
    return redirect('/blog/new')

@app.route('/blog/create', methods=['POST'])
def create_blog():
    """Handle blog post submission with validation."""
    if 'user_id' not in session:
        flash("You must be logged in to post.")
        return redirect('/login')

    # Validate input
    title = request.form.get("title", "").strip()
    content = request.form.get("content", "").strip()

    if not title or not content:
        flash("Title and content cannot be empty.")
        return redirect('/blog/new')

    # Store the user ID as the author (foreign key)
    data = {
        "title": title,
        "content": content,
        "author": session["user_id"]
    }

    BlogPost.save(data)
    return redirect('/blog')



@app.route('/like', methods=['POST'])
def like_post():
    # Ensure the user is logged in
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Please log in.'}), 403

    data = request.get_json()
    post_id = data.get('post_id')
    user_id = session.get('user_id')

    if not post_id:
        return jsonify({'success': False, 'message': 'No post provided'}), 400

    # Check whether the user has already liked this post.
    query = "SELECT * FROM post_likes WHERE user_id = %(user_id)s AND post_id = %(post_id)s;"
    check_data = {'user_id': user_id, 'post_id': post_id}
    result = connectToMySQL('project').query_db(query, check_data)

    if result and len(result) > 0:
        # Already liked—fetch the current like count and return without updating.
        query = "SELECT likes FROM blog_posts WHERE id = %(post_id)s;"
        res = connectToMySQL('project').query_db(query, {'post_id': post_id})
        current_likes = res[0]['likes'] if res and len(res) > 0 else 0
        return jsonify({
            'success': False, 
            'liked': True, 
            'likes': current_likes, 
            'message': 'Already liked'
        }), 200

    # Otherwise, increment the like count in the blog_posts table.
    query = "UPDATE blog_posts SET likes = likes + 1 WHERE id = %(post_id)s;"
    connectToMySQL('project').query_db(query, {'post_id': post_id})

    # Insert a new record into post_likes to record this user's like.
    query = "INSERT INTO post_likes (user_id, post_id) VALUES (%(user_id)s, %(post_id)s);"
    connectToMySQL('project').query_db(query, {'user_id': user_id, 'post_id': post_id})

    # Retrieve the updated like count.
    query = "SELECT likes FROM blog_posts WHERE id = %(post_id)s;"
    res = connectToMySQL('project').query_db(query, {'post_id': post_id})
    updated_likes = res[0]['likes'] if res and len(res) > 0 else 0

    return jsonify({'success': True, 'likes': updated_likes})

@app.route('/logout')
def logout():
    session.clear()
    
    # Optionally, you can flash a message to confirm logout
    flash("You have been logged out successfully.", "success")
    
    return redirect('/')
