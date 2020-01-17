from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pdb


app = Flask(__name__,instance_relative_config=False)
app.config['SQLALCHEMY_DATABASE_URI'] =  'postgresql://postgres:1747@localhost:5432/treasure_hunt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
from . import models
db.create_all()
from . import db

db.session.commit()
# pdb.set_trace()
# with app.app_context():
#     from . import db

#     db.create_all()
#     print('@@@@@@')