from flask import jsonify
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import random
from .__init__ import db
from .__init__ import bp

#MY TABLES
from .models import user as USR
from .models import treasure as TRS
from .models import own as OWN
from .models import market as MKT


# bp = Blueprint("login", __name__, url_prefix="/try")





# retrive attribute of usr according to usrname
def GetU(usr_name, attri):
  return USR.find_one({'_id':usr_name})[attri]
# retrive attribute of treasure according to tr_name
def GetTr(tr_name, attri):
  return TRS.find_one({'_id':tr_name})[attri]

# show the content of a collection
# for debugging
def dump(CLT):
  for i in CLT.find():
    print(i)
  return 0
# reset the collection MKT
# for debugging
@bp.route("/reset/<string:CLT>",methods=['GET'])
def reset(CLT):
  db[CLT].delete()
  dump(db[CLT])
  return "Market reset!"

# LOGIN & SHOW USR_INFO
# as all the accounts are created by myself, for convenience, password unused here
@bp.route("/<string:name>", methods=['GET'])
def login(name):
    IF_NEW = False
    # if it's a new usr, sign up for him and show IF_NEW tag
    if USR.find_one({'uid': name}) == 0:   
      USR.insert_one({'uid':name, 'money':0,'luck':0})
      IF_NEW = True
    info = USR.find_one({"_id":name})
    return jsonify({"new":IF_NEW,"info":info})
    # return "<p>Hello</p>"

# SHOW
@bp.route("/<string:name>/show",methods=['GET'])
def show(name):
  show = USR.find_one({"_id":name})
  return jsonify({'name':show['_id'], 'money':show['money']})


@bp.route("/<string:name>/work", methods=['GET'])
def work(name):
  FLAG = GetU(name,'FLAG_work')
  if FLAG:
    return "You have already worked today! Take a break~"
  work = GetU(name, 'work')
  money = GetU(name,'money')+work
  USR.update_many({"_id":name},{"$set":{"money":money,"FLAG_work":True}})
  print("money=",GetU(name,'money'))
  return jsonify({'money':money,"usr info":USR.find_one({"_id":name})})


# EXPLORE
@bp.route("/<string:name>/explore", methods=['GET'])
def explore(name):
  FLAG = GetU(name,'FLAG_explore')
  if FLAG:
    return "You have already obtained a piece today! Don't be greedy~"
  luck = GetU(name, 'luck')
  # usr has geater chance to get treasures with price in(0.7*luck, 1.2*luck)
  area = list(TRS.find({'price': {'$gt':0.7*luck, '$lt':1.2*luck}}))
  # print(area)
  area.extend(list(TRS.find({})))
  i = random.randint(0,len(area)-1)
  new_tr = area[i]
  case = GetU(name,'case')
  # print(type(case))
  # add new_tr to usr's case
  # suppose each treasure can be owned multiple times
  case.append(new_tr)
  USR.update_many({'_id':name},{'$set':{'case':case,'FLAG_explore':True}})
  recycle(name)
  return jsonify({'usr info': USR.find_one({"_id":name}),'get new treasure':area[i],'tr_num':len(GetU(name,'case'))})

  
# auto delete if treasure-number exceeds case capacity
# define case capacity=5
def recycle(name):
  case = GetU(name,'case')
  while len(case)>5:
    
    lowest=1000
    index=0
    for j in range(len(case)):
      c = case[j]
      if c['price']<lowest:
        index = j
        lowest = c['price']
    case.remove(case[index])
    USR.update_one({'_id':name},{'$set':{'case':case}})
    # print("@")
  return

# WEAR
# define wear_on capacity = 3
#  usr can wear no more than 1 piece lucky-treasure and
#  no more than 2 pieces working-treasures.
@bp.route("/<string:name>/wear/<string:tr_name>", methods=['GET'])
def wear(name,tr_name):
  # verify if the treasure is in case  
  case = GetU(name,'case')
  print(case)
  wear_on = GetU(name,'wear_on')
  print(wear_on)
  for i in case:
    if i['_id'] == tr_name:
      # Tag=1:lucky-treasure
      # Tag=0:working-treasure
      TAG = bool(i['luck'])
      # check num of wore-ons
      luck_num = 0
      working_num = 0
      for j in wear_on:
        if bool(j['luck']):
          luck_num += 1
        else:
          working_num += 1
      print(luck_num, working_num)
      if (TAG and luck_num) or ((not TAG) and (working_num ==2)):
        return " No space to wear on!"
      # update
      wear_on.append(i)
      case.remove(i)
      luck = i['luck'] + GetU(name, 'luck')
      work = i['work_ab'] + GetU(name, 'work')
      USR.update_many({'_id':name},{'$set':{'wear_on':wear_on, 'case':case, 'luck':luck, 'work':work}})
      print(USR.find_one({'_id':name}))
      return jsonify({'usr': name,'luck':luck,'work':work,'treasure wore on':GetU(name,'wear_on'),'treasures in case':GetU(name,'case')})
  return "Your treasure does not exist!"


# UNWEAR
@bp.route("/<string:name>/unwear/<string:tr_name>", methods=['GET'])
def unwear(name,tr_name):
  # verify if the treasure is in case  
  case = GetU(name,'case')
  print(case)
  wear_on = GetU(name,'wear_on')
  print(wear_on)
  for i in wear_on:
    if i['_id'] == tr_name:
      wear_on.remove(i)
      case.append(i)
      luck = GetU(name, 'luck') - i['luck']
      work = GetU(name, 'work') - i['work_ab']
      USR.update_many({'_id':name},{'$set':{'wear_on':wear_on, 'case':case, 'luck': luck, 'work':work}})
      recycle(name)
      return jsonify({'usr': name,'luck':luck,'work':work,'treasure wore on':GetU(name,'wear_on'),'treasures in case':GetU(name,'case')})
      break
  return "Your treasure is not wore on!"


# SALE
# treasures wore on CANNOT be saled
@bp.route("/<string:name>/sale/<string:tr_name>", methods=['GET'])
def sale(name,tr_name):
  case = GetU(name,'case')
  print(case)
  for i in case:
    if i['_id'] == tr_name:
      case.remove(i)
      USR.update_one({"_id": name},{"$set": {'case':case}})
      MKT.insert_one({"tr_onsale":tr_name, "saler":name})
      dump(MKT)
      return jsonify({"usr case":case,'tr num in case':len(GetU(name,'case'))})    
  dump(MKT)
  return "Cannot sell treasure you don't have!"


# UNSALE
@bp.route("/<string:name>/unsale/<string:tr_name>", methods=['GET'])
def unsale(name,tr_name):
  if MKT.delete_one({'saler':name,'tr_onsale':tr_name}):
    dump(MKT)
    tr = TRS.find_one({'_id':tr_name})
    print(type(tr))
    print(tr)
    case = GetU(name,'case')
    case.append(tr)
    USR.update_one({'_id':name},{'$set':{'case':case}})
    recycle(name)
    return jsonify({"usr case":GetU(name,'case'),'tr num in case':len(GetU(name,'case'))})
  else:   
    return "Cannot unsale treasure you've never sold!"

# BUY
# buy treasures from MKT
@bp.route("/<string:name>/buy/<string:tr_name>", methods=['GET'])
def buy(name,tr_name):
  dump(MKT)
  # customer buy sth. donnot specify saler, the system choose one randomly
  tr_mkt = MKT.find_one({'tr_onsale':tr_name})
  print("tr_mkt:\t")
  print(type(tr_mkt))
  if tr_mkt!=None:
    saler = tr_mkt['saler']
    tr = TRS.find_one({'_id':tr_name})
    price = tr['price']
    c_money = GetU(name,'money')

    print("costumer\t")
    print(USR.find_one({"_id":name}))
    print("\nsaler\t")
    print(USR.find_one({"_id":saler}))
    
    # If one buy sth. from himself, he should also obey the rule that his MONEY(currently) >= PRICE
    # otherwise, he can only get back the treasure by UNSALE way
    if c_money < price:
      return "You donnot have enough money!"
    MKT.delete_one(tr_mkt)
    case = GetU(name,'case')
    case.append(tr)
    c_money -= price
    USR.update_many({'_id':name},{'$set':{'case':case,'money':c_money}})
    s_money = GetU(saler,'money')
    s_money += price
    USR.update_one({'_id':saler},{'$set':{'money':s_money}})
    recycle(name)
    dump(MKT)
    return jsonify({"costumer":USR.find_one({"_id":name}),"saler":USR.find_one({"_id":saler})})
  else:   
    return "Cannot buy treasure not in the Market!"







  







