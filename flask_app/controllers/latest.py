# flask_app/controllers/latest.py

from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.latest_model import LatestPost
from flask_app.models.user_model import User
from datetime import datetime
from werkzeug.utils import secure_filename
import os

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS



def is_admin():
    return session.get('is_admin', False)


@app.context_processor
def inject_current_user():
    """
    Make `user` available in all templates.
 
    """
    user = None
    if session.get('user_id'):
        user = User.get_by_id({'id': session['user_id']})
    return dict(user=user)



@app.route('/latest/new')
def new_latest():
    # DEBUG dump
    print("SESSION AT /latest/new →", dict(session))

    if not is_admin():
        flash("Unauthorized!", "danger")
        return redirect('/')
    return render_template('new_latest.html')



@app.route('/latest/create', methods=['GET', 'POST'])
def create_latest():
    """Handle the form submission and insert a new LatestPost."""
    if not is_admin():
        flash("Unauthorized!", "danger")
        return redirect('/')
    
    title = request.form['title']
    body  = request.form['body']
    created_at = datetime.now()
    file = request.files.get('image')
    image_filename = None
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        save_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(save_path)
        image_filename = filename

    data = {
        'title':          title,
        'body':           body,
        'image':          image_filename,
        'created_at':     created_at
    }
    LatestPost.create(data)
    flash("New post published!", "success")
    return redirect('/home')

# ← send them to /home, not /


@app.route('/debug/user/<int:id>')
def debug_user_page(id):
    user = User.get_by_id({'id': id})
    return render_template('user_debug.html', user=user)

@app.route('/latest/<int:id>/delete', methods=['POST'])
def delete_latest(id):
    if not is_admin():
        flash('Unauthorized to delete posts', 'danger')
        return redirect('/')
    LatestPost.delete({'id':id})
    flash('Post Deleted')
    return redirect('/home')
