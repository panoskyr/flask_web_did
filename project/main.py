# main.py

import re
from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user
from project.models import User,Document
import json
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    docs=Document.query.filter_by(userId=current_user.id).all()
    if not docs==None:
        #pass the current user and the documents to his name
        return render_template('profile.html', name=current_user.name,docs=docs)
    return render_template('profile.html', name="No docs found")

@main.route('/profile',methods=["POST"])
@login_required
def profile_post():
    documentName=request.form['documentName']
    with open('project/did1.json', 'r') as myfile:
        dict=json.load(myfile)

    newDocument=Document(documentName=documentName,jsonFile=dict)
    current_user.docs.append(newDocument)

    try:
        db.session.add(newDocument)
        db.session.commit()
        return redirect('/profile'),201
    except:
        "Problem with saving document", 404

@main.route('/delete/<int:id>')
@login_required
def delete(id):
    docToDelete=Document.query.get_or_404(id)

    try:
        db.session.delete(docToDelete)
        db.session.commit()
        return redirect('/profile')
    except:
        return "Problem with deleting"