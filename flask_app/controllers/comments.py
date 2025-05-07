from flask import redirect, request, session, flash, render_template,jsonify
from flask_app import app
from flask_app.models.comment_model import Comment
from flask_app.models.blog import BlogPost
from flask_app.models.user_model import User



# Route to handle comment submissions on anyone's post.
@app.route('/blog/<int:post_id>/comment', methods=['POST'])
def add_comment(post_id):
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'You must be logged in to comment.'}), 403

    content = request.form.get("content", "").strip()
    if not content:
        return jsonify({'success': False, 'message': 'Comment cannot be empty.'}), 400

    data = {
        "content": content,
        "user_id": session["user_id"],
        "blog_post_id": post_id
    }

    Comment.save(data)

    return jsonify({'success': True, 'content': content, 'username': session.get('username', 'Unknown')})






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





