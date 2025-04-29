from flask import render_template, request, redirect, session
from flask_app import app
from flask_app.models.blog import BlogPost
from flask_app.models.user_model import User
from datetime import datetime
from flask import flash

@app.route('/blog')
def blog():
    """Display all blog posts with logged-in user."""
    posts = BlogPost.get_all()
    
    # Retrieve the logged-in user's username from session (if available)
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
        return redirect('/blog')  # Redirect to blog homepage or a custom 404 page

    return render_template('show_blog.html', post=post)

