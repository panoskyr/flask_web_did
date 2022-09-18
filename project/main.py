# main.py

from flask import Blueprint, render_template
from flask_login import login_required, current_user
from project.models import User,Document

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    docs=Document.query.filter_by(userId=current_user.id)
    if not docs==None:
        #pass the current user and the documents to his name
        return render_template('profile.html', name=current_user.name,docs=docs)
    return render_template('profile.html', name="No docs found")