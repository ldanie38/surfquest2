from flask import render_template, request, redirect, session, flash, jsonify
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_app.models.blog import BlogPost
from flask_app.models.user_model import User
from flask_app.models.comment_model import Comment
from datetime import datetime
from werkzeug.utils import secure_filename
import os
from flask import url_for
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER




def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/blog')
def blog_index():
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
    if 'user_id' not in session:
        flash("You must be logged in to post.", "warning")
        return redirect(url_for('login'))

    # 1) Validate form fields
    title   = request.form.get("title", "").strip()
    content = request.form.get("content", "").strip()
    if not title or not content:
        flash("Title and content cannot be empty.", "danger")
        return redirect(url_for('new_blog'))

    # 2) Build the data dict (DB column is `image`, not `image_url`)
    data = {
        "title":   title,
        "content": content,
        "author":  session["user_id"],
        "image":   None
    }

    # 3) Handle optional upload
    image_file = request.files.get("post_image")
    if image_file and image_file.filename and allowed_file(image_file.filename):
        filename  = secure_filename(image_file.filename)
        save_dir  = app.config['UPLOAD_FOLDER']
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, filename)
        image_file.save(save_path)
        data["image"] = filename

    # 4) Persist exactly once
    try:
        BlogPost.save(data)
        flash("Post created!", "success")
    except Exception as e:
        print("❌ SQL error in create_blog:", e)
        flash("Couldn’t save post.", "danger")

    return redirect(url_for('blog'))







@app.route('/like', methods=['POST'])
def like_post():
    # Ensure the user is logged in.
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Please log in.'}), 403

    data = request.get_json()
    post_id = data.get('post_id')
    user_id = session.get('user_id')

    if not post_id:
        return jsonify({'success': False, 'message': 'No post provided'}), 400

    check_data = {'user_id': user_id, 'post_id': post_id}
    
    # Check whether the user has already liked this post.
    query = "SELECT * FROM post_likes WHERE user_id = %(user_id)s AND post_id = %(post_id)s;"
    result = connectToMySQL('project').query_db(query, check_data)

    if result and len(result) > 0:
        # Already liked—so unlike the post.
        # Decrement the like count.
        query = "UPDATE blog_posts SET likes = likes - 1 WHERE id = %(post_id)s;"
        connectToMySQL('project').query_db(query, {'post_id': post_id})
        
        # Remove the like record.
        query = "DELETE FROM post_likes WHERE user_id = %(user_id)s AND post_id = %(post_id)s;"
        connectToMySQL('project').query_db(query, check_data)
        
        # Retrieve the updated like count.
        query = "SELECT likes FROM blog_posts WHERE id = %(post_id)s;"
        res = connectToMySQL('project').query_db(query, {'post_id': post_id})
        updated_likes = res[0]['likes'] if res and len(res) > 0 else 0
        
        return jsonify({
            'success': True,
            'liked': False,
            'likes': updated_likes,
            'message': 'Unliked'
        })
    else:
        # User hasn't liked the post yet; add a like.
        query = "UPDATE blog_posts SET likes = likes + 1 WHERE id = %(post_id)s;"
        connectToMySQL('project').query_db(query, {'post_id': post_id})
        
        # Insert a new like record.
        query = "INSERT INTO post_likes (user_id, post_id) VALUES (%(user_id)s, %(post_id)s);"
        connectToMySQL('project').query_db(query, check_data)
        
        # Retrieve the updated like count.
        query = "SELECT likes FROM blog_posts WHERE id = %(post_id)s;"
        res = connectToMySQL('project').query_db(query, {'post_id': post_id})
        updated_likes = res[0]['likes'] if res and len(res) > 0 else 0
        
        return jsonify({
            'success': True,
            'liked': True,
            'likes': updated_likes,
            'message': 'Liked'
        })



@app.route('/logout')
def logout():
    session.clear()
    
    # Optionally, you can flash a message to confirm logout
    flash("You have been logged out successfully.", "success")
    
    return redirect('/')
