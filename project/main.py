# main.py
import copy
import re
from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user
from project.models import User,Document
import json
from . import db
from project import didDoc
from sqlalchemy.orm.attributes import flag_modified

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
    #for the json file to change we need to get to top level domain
    #get the old verificationmethod list
    oldVerificationMethod=document.jsonFile["verificationMethod"]
    print("the old verificationMethod is {}".format(oldVerificationMethod))
    numberOfKeys=len(document.jsonFile["verificationMethod"])
    keyId=document.jsonFile["id"]+"#key"+str(numberOfKeys)
    controller=document.jsonFile["id"]
    #use json to not double encode the string
    newKey=json.loads(request.form["publicKey"])
    newKeyDict={
        "id":keyId,
        "type":"JsonWebKey2020",
        "controller":controller,
        "publicKeyJwk":newKey
    }
    oldVerificationMethod.append(newKeyDict)
    document.jsonFile["verificationMethod"]=oldVerificationMethod
    print("added ver method")

    try:
        #signal to the db that we have modified the jsonfile
        flag_modified(document, "jsonFile")
        db.session.commit()
        return redirect("/profile")
    except:
        return "no change"
    return redirect(request.url)
    # newkey=request.form["publicKey"]
    # print("the new key is:{}".format(newkey))
    # #document.jsonFile is a dict

    # keyNumber=len(document.jsonFile["verificationMethod"])+1
    # newVerMethod={
    #     "id":document.jsonFile["id"]+"#key-"+str(keyNumber),
    #     "type":"JsonWebKey2020",
    #     "controller":document.jsonFile["id"],
    #     "publicKeyJwk":newkey
    # }
    # document.jsonFile["verificationMethod"].append(newVerMethod)
    # #the did object has added the new key
    # print(document.jsonFile)
    # #the document.jsonFile IS changed
    # try:
    #     db.session.commit()
    #     return redirect(request.url)
    # except:
    #     return "Could not modify file"
    # #redirect to modify GET
    
