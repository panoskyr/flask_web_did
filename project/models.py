# models.py

from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    docs=db.relationship('Document', backref='user')
    

# class Docs(db.Model):
#     id=db.Column(db.Integer,primary_key=True)
#     #owner name is used from the input of the user
#     owner_name=db.Column(db.String(200),nullable=False,unique=True)
#     #A new json document table with ids and complete json documents only
#     json_document=db.Column(db.JSON)
#     date_created=db.Column(db.DateTime, default=datetime.utcnow)

#     def __repr__(self):
#             return '<Document with id %r>'% self.id

class Document(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    #use the id of the user as a foreign key on each document
    userId=db.Column(db.Integer, db.ForeignKey('user.id'))
    jsonFile=db.Column(db.JSON)





# class VerificationMethod(db.Model):
#     id=db.Column(db.Integer, primary_key=True)
#     id_string=db.Column(db.String(200),nullable=False)
#     type=db.Column(db.String(100), default="JsonWebKey2020")
#     controller=db.Column(db.String(200))
#     keyJSON=db.Column(db.JSON)




