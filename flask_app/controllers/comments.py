from flask import redirect, request, session, flash, render_template, jsonify
from flask_app import app
from flask_app.models.comment_model import Comment
from flask_app.models.blog import BlogPost
from flask_app.models.user_model import User

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
            # If there's no parent, it's a top-level comment.
            nested.append(comment)
    return nested

# Route to handle comment submissions (or reply submissions) via AJAX.
@app.route('/blog/<int:post_id>/comment', methods=['POST'])
def add_comment(post_id):
    # Ensure the user is logged in.
    if 'user_id' not in session:
        return jsonify({'success': False, 
                        'message': 'You must be logged in to comment.'}), 403

    # Check if the request is JSON or form-encoded.
    if request.is_json:
        data_payload = request.get_json()
        content = data_payload.get("content", "").strip()
        parent_comment_id = data_payload.get("parent_comment_id")
    else:
        content = request.form.get("content", "").strip()
        parent_comment_id = request.form.get("parent_comment_id")
    
    if not content:
        return jsonify({'success': False, 
                        'message': 'Comment cannot be empty.'}), 400

    data = {
        "content": content,
        "user_id": session["user_id"],
        "blog_post_id": post_id,
        "parent_comment_id": parent_comment_id if parent_comment_id else None
    }

    Comment.save(data)  # Save the comment (or reply) into the database.

    return jsonify({
        'success': True,
        'content': content,
        'username': session.get('username', 'Unknown'),
        'parent_comment_id': parent_comment_id
    })

# A separate route for comment creation using standard form submissions.
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

    Comment.save({
        "content": content,
        "user_id": session["user_id"],
        "blog_post_id": post_id
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

    # Convert the author's id to a username for display.
    user = User.get_by_id({"id": post.author}) or {}
    post.author_username = user.username if user else "Unknown"

    # Fetch all comments for the blog post (ensuring a list is returned).
    comments = Comment.get_by_post({"blog_post_id": id}) or []
    # Optionally, nest the comments before sending to the template:
    # comments = nest_comments(comments)

    return render_template('show_blog.html', post=post, comments=comments)
