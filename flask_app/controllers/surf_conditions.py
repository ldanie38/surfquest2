from flask import render_template, request, redirect, session, flash, jsonify
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app