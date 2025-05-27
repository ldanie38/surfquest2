from flask import render_template, request, redirect, session, flash, jsonify
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_app.models.blog import BlogPost
from flask_app.models.user_model import User
from flask_app.models.comment_model import Comment
from datetime import datetime
from werkzeug.utils import secure_filename
import os
from flask import url_for


@app.route('/places')
def places():
    return render_template('places.html')
