#!/usr/bin/env python3

import os
import sys
from flask import Flask
from func import bp
import threading
import time
import signal
import pymongo
import sys 

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =  'postgresql://postgres:1747@localhost:5432/treasure_hunt'
db = SQLAlchemy(app)
#MY COLUMNS
USR = db['usr']
MKT = db['market']
TRS = db['treasure']

'''def quit(signum, frame):
    print ("stop fusion")
    sys.exit()
'''
# TOMORROW
# start a new thread
def tomorrow():
    '''signal.signal(signal.SIGINT, quit)                                
    signal.signal(signal.SIGTERM, quit)'''
    # try:
    while 1:
        print("@\t")
        for name in ['u1','peggy','doge']:
            # 20s as a day
            USR.update_one({'_id':name},{'$set':{'FLAG_work':False}})
            USR.update_one({'_id':name},{'$set':{'FLAG_explore':False}})
        time.sleep(10)

timer=threading.Timer(0,tomorrow)
timer.start()

@app.route('/')
def hello_world():
    return "<h1>Hey dude, welcome to mygame!</h1>"

app.register_blueprint(bp)
app.run()
