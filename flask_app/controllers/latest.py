# flask_app/controllers/latest.py

from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.latest_model import LatestPost
from flask_app.models.user_model import User
from datetime import datetime



def is_admin():
    return session.get('is_admin', False)


@app.context_processor
def inject_current_user():
    """
    Make `user` available in all templates.
 
    """
    user = None
    if session.get('user_id'):
        user = User.get_by_id({'id': session['user_id']})
    return dict(user=user)



@app.route('/latest/new')
def new_latest():
    # DEBUG dump
    print("SESSION AT /latest/new →", dict(session))

    if not is_admin():
        flash("Unauthorized!", "danger")
        return redirect('/')
    return render_template('new_latest.html')



@app.route('/latest/create', methods=['POST'])
def create_latest():
    """Handle the form submission and insert a new LatestPost."""
    if not is_admin():
        flash("Unauthorized!", "danger")
        return redirect('/')
    data = {
        'title':      request.form['title'],
        'body':       request.form['body'],
        'created_at': datetime.now()
    }
    LatestPost.create(data)
    flash("New post published!", "success")
    return redirect('/home')

# ← send them to /home, not /


@app.route('/debug/user/<int:id>')
def debug_user_page(id):
    user = User.get_by_id({'id': id})
    return render_template('user_debug.html', user=user)
