# flask_app/controllers/comment_controller.py

from flask import (
    redirect, request, session, flash,
    render_template, jsonify, url_for
)
from flask_app import app
from flask_app.models.comment_model import Comment
from flask_app.models.blog import BlogPost
from flask_app.models.user_model import User
from werkzeug.utils import secure_filename
import os

# -----------------------
# Configuration & Helpers
# -----------------------

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_DIR = os.path.join(app.root_path, 'static', 'uploads')
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_DIR

def allowed_file(filename):
    return (
        '.' in filename and 
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    )

def save_upload(fileobj):
    """
    Save a FileStorage object into UPLOAD_FOLDER if allowed.
    Returns the bare filename or None.
    """
    if fileobj and fileobj.filename and allowed_file(fileobj.filename):
        fn = secure_filename(fileobj.filename)
        dest = os.path.join(app.config['UPLOAD_FOLDER'], fn)
        fileobj.save(dest)
        return fn
    return None

def nest_comments(comments):
    """
    Take a flat list of Comment instances (with .id & .parent_comment_id)
    and return only the top-level comments, each with a .children list.
    """
    comment_map = {c.id: c for c in comments}
    for c in comments:
        c.children = []
    nested = []
    for c in comments:
        if c.parent_comment_id and c.parent_comment_id in comment_map:
            comment_map[c.parent_comment_id].children.append(c)
        else:
            nested.append(c)
    return nested

# ---------------
# Blog index page
# ---------------

@app.route('/blog')
def blog():
    posts       = BlogPost.get_all()
    total_likes = BlogPost.get_total_likes()
    username    = session.get('username')

    post_comments = {}
    for post in posts:
        author = User.get_by_id({"id": post.author})
        post.author_username = author.username if author else "Unknown"
        raw_comments = Comment.get_by_post({"blog_post_id": post.id})
        post_comments[post.id] = nest_comments(raw_comments)

    return render_template(
        'blog.html',
        posts=posts,
        username=username,
        total_likes=total_likes,
        post_comments=post_comments
    )

# -----------------------
# AJAX & Form comment API
# -----------------------

@app.route('/blog/<int:post_id>/comment', methods=['POST'])
def add_comment(post_id):
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Login required'}), 403

    # Choose between JSON payload (AJAX) or form data
    if request.is_json:
        payload = request.get_json()
    else:
        payload = request.form

    content   = payload.get('content', '').strip()
    parent_id = payload.get('parent_comment_id') or None
    



    # Save either a top-level or nested image
    fileobj  = request.files.get('comment_image') or request.files.get('reply_image')
    filename = save_upload(fileobj)

    # Persist the comment
    data = {
        'content':            content,
        'user_id':            session['user_id'],
        'blog_post_id':       post_id,
        'parent_comment_id':  parent_id,
        'image_url':          filename
    }
    Comment.save(data)

    # Build the public URL to return in JSON
    public_url = (
        url_for('static', filename=f"uploads/{filename}")
        if filename else None
    )
    resp = {
        'success':           True,
        'content':           content,
        'username':          session.get('username'),
        'parent_comment_id': parent_id,
        'image_url':         public_url
    }

    # AJAX callers get JSON, normal form gets redirected view
    if request.is_json:
        return jsonify(resp)
    if not request.is_json:
        print("→ FORM keys:", request.form.keys())
        print("→ FILES keys:", request.files.keys())




    return redirect(url_for('show_blog', id=post_id))

# ---------------------------
# Classic form‐only comment
# ---------------------------

@app.route('/comment/create', methods=['POST'])
def create_comment():
    if 'user_id' not in session:
        flash("Login required", "warning")
        return redirect('/blog')

    content = request.form.get('content', '').strip()
    post_id = request.form.get('post_id')
    parent  = request.form.get('parent_comment_id') or None

    filename = save_upload(
        request.files.get('comment_image')
        or request.files.get('reply_image')
    )

    Comment.save({
        'content':            content,
        'user_id':            session['user_id'],
        'blog_post_id':       post_id,
        'parent_comment_id':  parent,
        'image_url':          filename
    })
    return redirect(url_for('show_blog', id=post_id))

# ----------------
# Single‐post page
# ----------------

@app.route('/blog/<int:id>')
def show_blog(id):
    post = BlogPost.get_by_id({"id": id})
    if not post:
        flash("Post not found", "warning")
        return redirect(url_for('blog'))

    author = User.get_by_id({"id": post.author})
    post.author_username = author.username if author else "Unknown"

    raw_comments    = Comment.get_by_post({"blog_post_id": post.id})
    nested_comments = nest_comments(raw_comments)

    return render_template(
        'show_blog.html',
        post=post,
        comments=nested_comments
    )
