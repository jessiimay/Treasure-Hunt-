#!/usr/bin/env python3
import flask as Flask
from flask.testing import FlaskClient
import random
import pymongo
from mongoengine import *
import pdb

myclient = pymongo.MongoClient('mongodb://localhost:27017/')
db = myclient['mygame']
#MY COLUMNS
USR = db['usr']
MKT = db['market']
TRS = db['treasure']


# INIT
# create a state of database
name = '海绵宝宝'
# APP = Flask(__name__)
# APP.config['MONGODB_SETTINGS'] = {
#     "db": "mygame"
# }
# DB = MongoEngine(APP)
# usr(uid=name, money=100, luck=100,work=100).save()



# retrive attribute of usr according to usrname
def GetU(usr_name, attri):
  return USR.find_one({'_id':usr_name})[attri]
# retrive attribute of treasure according to tr_name
def GetTr(tr_name, attri):
  return TRS.find_one({'_id':tr_name})[attri]


def test_work(client: FlaskClient):
    pdb.set_trace()
    FLAG = GetU(name,'FLAG_work')
    work = GetU(name,'work')
    money = GetU(name,'money')
   # print("money=",money)
    if FLAG==False:
        money += work
    response = client.get("/try/%s/work" % (name))
    json = response.get_json()
   # print("josn_money=",json['money'])
    print(json)
    assert json['money']==money

'''

def test_explore(client: FlaskClient):
    print(2)
    FLAG = GetU(name,'FLAG_explore')
    case = GetU(name,'case')
    lenth = len(case)
    if FLAG==False and lenth<5:
        lenth += 1        
    response = client.get("/try/%s/explore" % (name))
    json = response.get_json()
    assert json['tr_num']==len(GetU(name,'case'))


def test_wear(client: FlaskClient):
    print(3)
    case = GetU(name,'case')
    wear_on = GetU(name,'wear_on')
    luck = GetU(name,'luck')
    work = GetU(name,'work')
    # define max length reserve
    luck_num = 1
    work_num = 2
    for i in wear_on:
        luck_num -= bool(i['luck'])
        work_num -= bool(i['work_ab'])
    index = random.randint(0,len(case)-1)
    new_tr = case[index]
    new_tr_name = new_tr['_id']
    luck_num -= bool(new_tr['luck'])
    work_num -= bool(new_tr['work_ab'])
    if luck_num>=0 and work_num>=0:
        luck += new_tr['luck']
        work += new_tr['work_ab']
    response = client.get("/try/%s/wear/%s" % (name,new_tr_name))
    json = response.get_json()
    if json['luck']:# print(type(json['luck']))
    # print(json['luck'])
        assert json['luck']==luck
    if json['work']:
        assert json['work']==work

def test_unwear(client: FlaskClient):
    print(4)
    wear_on = GetU(name,'wear_on')
    index = random.randint(0,len(wear_on)-1)
    tr = wear_on[index]
    tr_name = tr['_id']
    luck = GetU(name,'luck')-tr['luck']
    work = GetU(name,'work')-tr['work_ab']
    response = client.get("/try/%s/unwear/%s" % (name,tr_name))
    json = response.get_json()
    assert json['luck']==luck
    assert json['work']==work


def test_sale(client: FlaskClient):
    print(5)
    # case = GetU(name,'case')
    # case_num = len(case)
    # index = random.randint(0,case_num-1)
    # tr = case[index]
    tr = TRS.find_one({'name':"t8"})
    tr_name = 't8'
    mkt_num = len(list(MKT.find({'tr_onsale':tr_name,'saler':name})))
    response = client.get("/try/%s/sale/%s" % (name,tr_name))
    json = response.get_json()
    new_mkt_num = len(list(MKT.find({'tr_onsale':tr_name,'saler':name})))
    assert mkt_num+1 == new_mkt_num
    assert case_num-1 == json['tr num in case']

def test_unsale(client: FlaskClient):
    print(6)
    case = GetU(name,'case')
    case_num = len(case)
    area = list(MKT.find({"saler":name}))
    index = random.randint(0,len(area)-1)
    tr = area[index]
    tr_name = tr['_id']
    mkt_num = len(list(MKT.find({"saler":name,"tr_onsale":tr_name})))
    response = client.get("/try/%s/unsale/%s" % (name,tr_name))
    json = response.get_json()
    new_mkt_num = len(list(MKT.find({"saler":name,"tr_onsale":tr_name})))
    assert mkt_num-1 == new_mkt_num
    assert case_num+1 == json['tr num in case']

def test_buy(client: FlaskClient):
    print(7)
    c_money = GetU(name,'money')
    area = list(MKT.find({}))
    index = random.randint(0,len(area)-1)
    while(GetTr(area[index]['tr_onsale'],'price') > c_money):
        area.remove(area[index])
        index = random.randint(0,len(area))
    tr_name = area[index]['tr_onsale']
    # saler = area[index]['saler']
    price = GetTr(tr_name,'price')
    # s_money = GetU(saler,'money')
    response = client.get("/try/%s/buy/%s" % (name,tr_name))
    json = response.get_json()
    s_money = json['saler']['money']
    if name!=saler:
        assert s_money >= price
        assert c_money+price == json['costumer']['money']
    else:
        assert json['costumer'] == json['saler']
'''