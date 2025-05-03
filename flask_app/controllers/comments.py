from flask import redirect, request, session, flash, render_template
from flask_app import app
from flask_app.models.comment_model import Comment
from flask_app.models.blog import BlogPost
from flask_app.models.user_model import User



# Route to handle comment submissions on anyone's post.
@app.route('/blog/<int:post_id>/comment', methods=['POST'])
def add_comment(post_id):
    # Require user to be logged in.
    if 'user_id' not in session:
        flash("You must be logged in to comment.", "danger")
        return redirect('/login')
    
    # Get and validate the comment content from the form.
    content = request.form.get("content", "").strip()
    if not content:
        flash("Comment cannot be empty.", "danger")
        return redirect(f'/blog/{post_id}')
    
    # Prepare data for saving the comment.
    data = {
        "content": content,
        "user_id": session["user_id"],
        "blog_post_id": post_id
    }
    
    # Save the comment using the Comment model.
    Comment.save(data)
    flash("Comment added successfully.", "success")
    
    # Redirect back to the blog post page to show the updated comments.
    return redirect(f'/blog/{post_id}')



