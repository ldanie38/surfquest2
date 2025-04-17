from flask import Flask,render_template,request,session,redirect
from flask_app import app
#from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from datetime import datetime
from flask import flash
import os
from pprint import pprint