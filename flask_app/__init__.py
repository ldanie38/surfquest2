from flask import Flask
import os
app = Flask(__name__)
app.secret_key = "secreto"
app.config["UPLOAD_FOLDER"] = os.path.join(app.root_path, "static", "uploads")

# Ensure the upload folder exists.
upload_folder = app.config.get("UPLOAD_FOLDER")
if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)
    
UPLOAD_FOLDER = os.path.join(app.static_folder, 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# 1. Point to static/uploads
UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')

# 2. Make sure the folder exists on disk
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 3. Store it in your config for easy access
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


