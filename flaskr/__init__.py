from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pdb
# from .func import bp
import threading
import time
from flask import Blueprint

app = Flask(__name__,instance_relative_config=False)
app.config['SQLALCHEMY_DATABASE_URI'] =  'postgresql://postgres:1747@localhost:5432/treasure_hunt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
from . import models
db.create_all()
from . import db


# db.session.commit()
# pdb.set_trace()
# with app.app_context():
#     from . import db

#     db.create_all()
#     print('@@@@@@')
def tomorrow():
    '''signal.signal(signal.SIGINT, quit)                                
    signal.signal(signal.SIGTERM, quit)'''
    # try:
    while 1:
        print("@\t")
        for name in ['u1','peggy','doge']:
            # 10s as a day
            u_tmp = user.query.filter_by(uid=name)
            u_tmp.FLAG_work = False
            u_tmp.FLAG_explore = False
            # db.session.flush()
            db.session.commit()
        time.sleep(10)

timer=threading.Timer(0,tomorrow)
timer.start()

@app.route('/')
def hello_world():
    return "<h1>Hi friend, welcome to Treasure Hunt!  Begin your exploration now~</h1>"
bp = Blueprint("login", __name__, url_prefix="/try")
app.register_blueprint(bp)
app.run()