from flask_app.controllers import users
from flask_app.controllers import blogs
from flask_app.controllers import comments
from flask_app.controllers import surf_conditions
from flask_app.controllers import places
from flask_app.controllers import latest
from flask_app.controllers import main
from flask_app import app 
from flask import session
from flask_app.models.user_model import User
import os
from dotenv import load_dotenv


load_dotenv()  # This loads the variables from your .env file

GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
DATABASE_URL = os.environ.get('DATABASE_URL')

@app.context_processor
def inject_current_user():
    user = None
    if session.get('user_id'):
        # Fetch the user from the DB once per request
        user = User.get_by_id({'id': session['user_id']})
    return dict(user=user)



UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 2. Make sure the folder exists on disk
os.makedirs(UPLOAD_FOLDER, exist_ok=True)






if __name__ == "__main__":
    port = int(os.getenv("PORT", 5001))  # Default to 5000 if PORT isn't set
    app.run(host="0.0.0.0", port=port)