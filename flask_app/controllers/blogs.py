from flask import render_template, request, redirect, session, flash, jsonify
from flask_app import app
from flask_app.models.blog import BlogPost
from flask_app.models.user_model import User
from datetime import datetime

@app.route('/blog')
def blog():
    """Display all blog posts with logged-in user."""
    posts = BlogPost.get_all()

    # Convert the stored user ID to a username for display
    # (Add a new attribute 'author_username' on each post)
    for post in posts:
        user = User.get_by_id({"id": post.author})
        post.author_username = user.username if user else "Unknown"

    # Retrieve the logged-in user's username from session
    username = session.get("username", None)
    return render_template('blog.html', posts=posts, username=username)

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

@app.route('/blog/<int:id>')
def show_blog(id):
    """View a single blog post and handle missing posts."""
    data = {"id": id}
    post = BlogPost.get_by_id(data)

    if not post:
        flash("Blog post not found.")
        return redirect('/blog')

    # Also convert the author ID to a username for display on the single-post page
    user = User.get_by_id({"id": post.author})
    post.author_username = user.username if user else "Unknown"

    return render_template('show_blog.html', post=post)

@app.route('/like', methods=['POST'])
def like_post():
    data = request.get_json()
    post_id = data.get('post_id')
    
    if not post_id:
        return jsonify({'success': False}), 400
    
    # Increment the post's like count.
    updated_like_count = BlogPost.increment_like(post_id)
    if updated_like_count is not None:
        return jsonify({'success': True, 'likes': updated_like_count})
    else:
        return jsonify({'success': False}), 500

@app.route('/logout')
def logout():
    session.clear()
    
    # Optionally, you can flash a message to confirm logout
    flash("You have been logged out successfully.", "success")
    
    return redirect('/')
