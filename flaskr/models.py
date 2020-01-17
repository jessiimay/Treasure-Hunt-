from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime
from .__init__ import db

class user(db.Model):
    uid = db.Column(db.String(100), primary_key=True)
    FLAG_work = db.Column(db.Boolean)
    FLAG_explore = db.Column(db.Boolean)
    money = db.Column(db.Integer)
    luck = db.Column(db.Integer)
    work = db.Column(db.Integer)
    tr_num = db.Column(db.Integer)

    def __init__(self, uid, money, luck, work):
        self.uid = uid
        self.FLAG_work = False
        self.FLAG_explore = False
        self.money = money
        self.luck = luck
        self.work = work
        self.tr_num = 0
    
    def __repr__(self):
        return "uid:%s, FLAG_work:%r, FLAG_explore:%r, money:%d, luck:%d, work:%d, treasure number:%d" % (
            self.uid, self.FLAG_work, self.FLAG_explore, self.money, self.luck, self.work, self.tr_num)

class treasure(db.Model):
    tid = db.Column(db.String(100), primary_key=True)
    luck = db.Column(db.Integer)
    work = db.Column(db.Integer)
    price = db.Column(db.Integer,index=True)

    def __init__(self, tid, luck, work, price):
        self.tid = tid
        self.luck = luck
        self.work = work
        self.price = price

    def __repr__(self):
        return "tid:%s, luck:%d, work:%d, price:%d" % (
            self.tid, self.luck, self.work, self.price)


class own(db.Model):
    oid = db.Column(db.String(100), primary_key=True)
    uid = db.Column(db.String(100), db.ForeignKey('user.uid'),index=True)
    tid = db.Column(db.String(100), db.ForeignKey('treasure.tid'),index=True)
    wearing_state = db.Column(db.Boolean)
    
    def __init__(self,uid,tid):
        self.oid = uid+'#'+tid+'#'+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.uid = uid
        self.tid = tid
        self.wearing_state = False

    def __repr__(self):
        return "uid:%s, tid:%s, wearing state:%r" % (
            self.uid, self.tid, self.wearing_state)

class market(db.Model):
    mid = db.Column(db.String(200), primary_key=True)
    tid = db.Column(db.String(100), db.ForeignKey('treasure.tid'),index=True)
    seller = db.Column(db.String(100), db.ForeignKey('user.uid'),index=True)
    buyer = db.Column(db.String(100))

    def __init__(self,seller,tid):
        self.mid = seller+'#'+tid+'#'+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.tid = tid
        self.seller = seller
        self.buyer = ''

    def __repr__(self):
        return "tid:%s, seller:%d, buyer:%s" % (
            self.tid, self.seller, self.buyer)

    # def sold():
    #     if self.buyer.strip():
    #         return True
    #     else:
    #         return False

        

