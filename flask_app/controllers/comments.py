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





@app.route('/blog/<int:id>')
def show_blog(id):
    data = {"id": id}
    post = BlogPost.get_by_id(data)

    if not post:
        flash("Blog post not found.")
        return redirect('/blog')

    user = User.get_by_id({"id": post.author}) or {}
    post.author_username = user.username if user else "Unknown"


    # Fetch all comments for this post, ensuring it's always a list
    comments = Comment.get_by_post({"blog_post_id": id}) or []

    return render_template('show_blog.html',post=post, comments=comments)





