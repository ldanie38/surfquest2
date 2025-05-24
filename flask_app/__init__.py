from flask import Flask
import os
app = Flask(__name__)
app.secret_key = "secreto"
app.config["UPLOAD_FOLDER"] = os.path.join(app.root_path, "static", "uploads")

# Ensure the upload folder exists.
upload_folder = app.config.get("UPLOAD_FOLDER")
if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)


