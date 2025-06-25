from flask_app.models.latest_model import LatestPost
from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.latest_model import LatestPost

from datetime import datetime

@app.route('/')
def latest_home():
    latest_posts = LatestPost.get_all()[:3]   # show only the 3 newest
    # … any other data you pass …
    return render_template('home.html', latest_posts=latest_posts)
