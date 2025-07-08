from flask_app.models.latest_model import LatestPost
from flask import render_template, request, redirect, session, flash, url_for
from flask_app import app
from werkzeug.utils import secure_filename
from flask_app.models.latest_model import LatestPost
import os

app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # limit to 5 MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
from datetime import datetime

@app.route('/')
def latest_home():
    latest_posts = LatestPost.get_all()[:3]   # show only the 3 newest
    # … any other data you pass …
    return render_template('home.html', latest_posts=latest_posts)

