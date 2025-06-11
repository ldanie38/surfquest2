from flask_app.controllers import users
from flask_app.controllers import blogs
from flask_app.controllers import comments
from flask_app.controllers import surf_conditions
from flask_app.controllers import places
from flask_app import app 
import os
from dotenv import load_dotenv


load_dotenv()  # This loads the variables from your .env file

GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
DATABASE_URL = os.environ.get('DATABASE_URL')





if __name__ == "__main__":
    port = int(os.getenv("PORT", 5001))  # Default to 5000 if PORT isn't set
    app.run(host="0.0.0.0", port=port)