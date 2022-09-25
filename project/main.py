# main.py

import re
from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user
from project.models import User,Document
import json
from . import db
from project import didDoc

main = Blueprint('main', __name__)

def convert(url):
    url=url
    convertedUrl=url[7:]
    convertedUrl=convertedUrl.replace('/', ':')
    convertedUrl='did:web:'+ convertedUrl
    return convertedUrl

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
    publicKey=request.form['publicKey']
    #a dictionary of the public key given as input
    publicKey=json.loads(publicKey)
    print("the public key as input is :{}".format(publicKey))
    ownername=current_user.name
    url='http://localhost%A35000/'+ownername+'/'+documentName
    
    with open('project/did2.json', 'r') as myfile:
        didDict=json.load(myfile)


    did=didDoc.DID(didDict)
    did.id=convert(url)
    did.verificationMethod[0]["publicKeyJwk"]=publicKey
    did.verificationMethod[0]["id"]=did.id+"#key-"+str(len(did.verificationMethod)+1)
    did.verificationMethod[0]["controller"]=did.id
    newDocument=Document(documentName=documentName,jsonFile=did.to_json())
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

@main.route('/<owner>/<documentName>/did.json')
def show_did(owner,documentName):
    user=User.query.filter_by(name=owner).first()
    document=Document.query.filter_by(documentName=documentName).first()
    return render_template('show_did.html',did=document.jsonFile)
    
@main.route('/modify/<int:id>')
@login_required
def modify(id):
    document=Document.query.get_or_404(id)
    #pass a document class object
    #access the jsonFIle from the html file
    return render_template('modify.html',did=document)

@main.route('/modify/<int:id>',methods=["POST"])
@login_required
def modify_post(id):
    document=Document.query.get_or_404(id)
    newkey=request.form["publicKey"]
    print("the new key is:{}".format(newkey))
    #document.jsonFile is a dict
    did=document.jsonFile
    keyNumber=len(did["verificationMethod"])+1
    newVerMethod={
        "id":did["id"]+"#key-"+str(keyNumber),
        "type":"JsonWebKey2020",
        "controller":did["id"],
        "publicKeyJwk":newkey
    }
    did["verificationMethod"].append(newVerMethod)
    #the did object has added the new key
    document.jsonFile=did
    print(document.jsonFile)
    #the document.jsonFile IS changed
    try:
        db.session.commit()
        d=Document.query.get_or_404(id)
        print(d.jsonFile["verificationMethod"][-1])
    except:
        return "Could not modify file"
    #redirect to modify GET
    return redirect(request.url)
