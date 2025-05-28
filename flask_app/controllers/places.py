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
import os
from dotenv import load_dotenv
import requests


load_dotenv()  # Load environment variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")






@app.route('/places')
def places():
    return render_template('places.html')


@app.route('/search_places')
def search_places():
    query = request.args.get('query')
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}&key={GOOGLE_API_KEY}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        print(data)  # 🔍 Debug output

        return jsonify(data)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Failed to fetch places", "details": str(e)})


