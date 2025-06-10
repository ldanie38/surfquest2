from flask_app.controllers import users
from flask_app.controllers import blogs
from flask_app.controllers import comments
from flask_app.controllers import surf_conditions
from flask_app.controllers import places
from flask_app import app 
import os




if __name__ == "__main__":
    # Heroku sets the PORT dynamically, fallback to 4242 for local dev
    PORT = int(os.getenv("PORT", 4242))
    app.run(debug=True, host="0.0.0.0", port=PORT)