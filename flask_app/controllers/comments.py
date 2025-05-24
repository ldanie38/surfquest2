from flask import redirect, request, session, flash, render_template, jsonify, url_for
from flask_app import app
from flask_app.models.comment_model import Comment
from flask_app.models.blog import BlogPost
from flask_app.models.user_model import User
from werkzeug.utils import secure_filename
import os

def nest_comments(comments):
    """
    Given a flat list of comment objects, rearrange them so that each comment
    includes a .children attribute with its replies.
    """
    comment_map = {}
    for comment in comments:
        comment.children = []  # initialize the children list
        comment_map[comment.id] = comment

    nested = []
    for comment in comments:
        if comment.parent_comment_id:  # It's a reply.
            parent = comment_map.get(comment.parent_comment_id)
            if parent:
                parent.children.append(comment)
        else:
            nested.append(comment)
    return nested

# Route to handle comment/reply submissions via AJAX.
@app.route('/blog/<int:post_id>/comment', methods=['POST'])
def add_comment(post_id):
    # Ensure the user is logged in.
    if 'user_id' not in session:
        return jsonify({'success': False, 
                        'message': 'You must be logged in to comment.'}), 403

    # Determine if the request is JSON or form-encoded.
    if request.is_json:
        data_payload = request.get_json()
        content = data_payload.get("content", "").strip()
        parent_comment_id = data_payload.get("parent_comment_id")
        image_url = None  # File uploads are not sent via JSON.
    else:
        content = request.form.get("content", "").strip()
        # Get the parent comment ID if this is a reply.
        parent_comment_id = request.form.get("parent_comment_id")
        
        # This is where the image file is handled.
        image_file = request.files.get("comment_image") or request.files.get("reply_image")
        image_url = None
        if image_file and image_file.filename:
            filename = secure_filename(image_file.filename)
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            image_file.save(file_path)
            image_url = url_for('static', filename=f"uploads/{filename}")
    
    # (Additional logic for validating and saving the comment)
    data = {
        "content": content,
        "user_id": session["user_id"],
        "blog_post_id": post_id,
        "parent_comment_id": parent_comment_id if parent_comment_id else None,
        "image_url": image_url
    }
    Comment.save(data)
    return jsonify({
        'success': True,
        'content': content,
        'username': session.get('username', 'Unknown'),
        'parent_comment_id': parent_comment_id,
        'image_url': image_url
    })


# Traditional route for comment creation (standard form submission).
@app.route('/comment/create', methods=['POST'])
def create_comment():
    if 'user_id' not in session:
        flash("You must be logged in to comment.")
        return redirect('/blog')

    content = request.form.get("content", "").strip()
    post_id = request.form.get("post_id")

    if not content:
        flash("Comment cannot be empty.")
        return redirect(f'/blog/{post_id}')

    # Process file upload from the form.
    image_file = request.files.get("comment_image") or request.files.get("reply_image")
    image_url = None
    if image_file and image_file.filename:
        filename = secure_filename(image_file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        image_file.save(file_path)
        image_url = url_for('static', filename=f"uploads/{filename}")

    Comment.save({
        "content": content,
        "user_id": session["user_id"],
        "blog_post_id": post_id,
        "image_url": image_url
    })

    return redirect(f'/blog/{post_id}')

# Route to display a single blog post along with its comments.
@app.route('/blog/<int:id>')
def show_blog(id):
    data = {"id": id}
    post = BlogPost.get_by_id(data)

    if not post:
        flash("Blog post not found.")
        return redirect('/blog')

    # Get the author's username.
    user = User.get_by_id({"id": post.author}) or {}
    post.author_username = user.username if user else "Unknown"

    # Fetch comments (optionally, you could nest them).
    comments = Comment.get_by_post({"blog_post_id": id}) or []
    # comments = nest_comments(comments)  # Uncomment if you want nested comments
    
    return render_template('show_blog.html', post=post, comments=comments)


