from flask import Flask
from flask_mongoengine import MongoEngine
from mongoengine import *

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    "db": "mygame"
}
db = MongoEngine(app)

class treasure(Document):
    tr_name = StringField(required = True,primary_key=True)
    luck = IntField()
    work_ab = IntField()
    price = IntField(required = True)

class usr(Document):
    FLAG_explore = BooleanField(default=False)
    FLAG_work = BooleanField(default=False)
    uid = StringField(required = True,primary_key=True)
    money = IntField(required = True)
    luck = IntField(required = True)
    work = IntField(default = 0)
    case = ListField(default=list)
    wear_on = ListField(default=list)

class market(Document):
    tr_onsale = StringField(required=True)
    saler = StringField(required=True)


# db.save()
# db.objects(type="usr").delete()
# db.objects(type='market').delete()

# my_collection.usr.objects.delete()
# usr.save()

t1=treasure('陈诺的数学笔记', 0, 50, 50)
t1.save()
t2=treasure('曹汇杰的智慧', 0, 100, 100)
t2.save()
t3=treasure('import*from邹弘嘉', 0, 150, 150)
t3.save()
t4=treasure('周烜的祝福', 60, 0, 60)
t4.save()
t5=treasure('哈库拉玛塔塔',30, 0, 30)
t5.save()
t6=treasure('t6', 20, 0 ,20)
t6.save()
t7=treasure('t7',0, 40, 40)
t7.save()
t8=treasure('t8',80, 0, 80)
t8.save()
usr(uid='doge', money=0, luck=0).save()
usr(uid='peggy', money=80, luck=40).save()
usr(uid='海绵宝宝', money=120, luck=20,work=40,case=[t6,t7,t8],wear_on=[t1]).save()    
market(tr_onsale='t6',saler='peggy').save()
market(tr_onsale='t7',saler='doge').save()
market(tr_onsale='t8',saler='海绵宝宝').save()
