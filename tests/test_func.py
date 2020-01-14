#!/usr/bin/env python3
import flask as Flask
from flask.testing import FlaskClient
# import sys
# sys.path.append('../')
# import flaskr.app
import pytest
import os
import tempfile
import random
import pymongo
from mongoengine import *
import pdb

myclient = pymongo.MongoClient('mongodb://localhost:27017/')
db = myclient['treasure_hunt']
#MY COLUMNS
USR = db['usr']
MKT = db['market']
TRS = db['treasure']


# INIT
# create a state of database
name_1 = 'peggy'
name_2 = 'doge'



# retrive attribute of usr according to usrname
def GetU(usr_name, attri):
  return USR.find_one({'_id':usr_name})[attri]
# retrive attribute of treasure according to tr_name
def GetTr(tr_name, attri):
  return TRS.find_one({'_id':tr_name})[attri]


def test_work(client: FlaskClient):
    # pdb.set_trace()
    FLAG = GetU(name_1,'FLAG_work')
    work = GetU(name_1,'work')
    money = GetU(name_1,'money')
   # print("money=",money)
    if FLAG==False:
        money += work
    response = client.get("/try/%s/work" % (name_1))
    json = response.get_json()
   # print("josn_money=",json['money'])
    print(json)
    assert json['money']==money



def test_explore(client: FlaskClient):
    print(2)
    FLAG = GetU(name_1,'FLAG_explore')
    case = GetU(name_1,'case')
    lenth = len(case)
    if FLAG==False and lenth<5:
        lenth += 1        
    response = client.get("/try/%s/explore" % (name_1))
    json = response.get_json()
    assert json['tr_num']==len(GetU(name_1,'case'))


def test_wear(client: FlaskClient):
    print(3)
    case = GetU(name_1,'case')
    wear_on = GetU(name_1,'wear_on')
    luck = GetU(name_1,'luck')
    work = GetU(name_1,'work')
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
    response = client.get("/try/%s/wear/%s" % (name_1,new_tr_name))
    json = response.get_json()
    if json['luck']:# print(type(json['luck']))
    # print(json['luck'])
        assert json['luck']==luck
    if json['work']:
        assert json['work']==work

def test_unwear(client: FlaskClient):
    print(4)
    wear_on = GetU(name_1,'wear_on')
    index = random.randint(0,len(wear_on)-1)
    tr = wear_on[index]
    tr_name = tr['_id']
    luck = GetU(name_1,'luck')-tr['luck']
    work = GetU(name_1,'work')-tr['work_ab']
    response = client.get("/try/%s/unwear/%s" % (name_1,tr_name))
    json = response.get_json()
    assert json['luck']==luck
    assert json['work']==work


def test_sale_and_unsale(client: FlaskClient):
    print(5)
    case = GetU(name_1,'case')
    case_num = len(case)
    index = random.randint(0,case_num-1)
    tr = case[index]

    # pdb.set_trace()
    tr_name = tr['_id']
    mkt_num = len(list(MKT.find({'tr_onsale':tr_name,'saler':name_2})))
    response = client.get("/try/%s/sale/%s" % (name_1,tr_name))
    json = response.get_json()
    new_mkt_num = len(list(MKT.find({'tr_onsale':tr_name,'saler':name_2})))
    assert case_num-1 == json['tr num in case']

    # pdb.set_trace()
    response2 = client.get("/try/%s/unsale/%s" % (name_1,tr_name))
    json2 = response2.get_json()
    new_mkt_num = len(list(MKT.find({"saler":name_1,"tr_onsale":tr_name})))
    assert case_num == json2['tr num in case']



'''the piece of treasure bought here is initialized with creat_db action,
     so we can specify its name and saler in advance.
     Make sure that the customor's money is sufficient 
     to buy a piece of treasure from the (specified) saler.'''
def test_buy(client: FlaskClient):
    print(7)
    c_money = GetU(name_1,'money')
    tr_name = 't8'
    saler = name_2
    price = GetTr(tr_name,'price')
    s_money = GetU(saler,'money')#saler's money
    # pdb.set_trace()
    response = client.get("/try/%s/buy/%s" % (name_1,tr_name))
    json = response.get_json()
    assert s_money+price == json['saler']['money']
    assert c_money-price == json['costumer']['money']
