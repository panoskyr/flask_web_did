- activate the python env
- set FLASK_APP=project
- set FLASK_DEBUG=TRUE
- flask shell
  - from project import db
  - from project.models import User,Document
  - db.create_all()
- flask run