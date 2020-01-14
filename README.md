# Treasure Hunt! @基于mongoDB的实现

## 代码组织

- 文件目录：

  |——flaskr

  ​		|————\_init\_.py

  ​		|————app.py		另起线程实现“每天”的流逝

  ​		|————db.py 		将创建数据库（的某个状态）分离出来

  ​		|————func.py		用户功能实现

  |——tests

  ​		|————\_init\_.py

  ​		|————conftest.py	定义client

  ​		|————test_func.py	测试用户功能

  |——venv								环境

  |——README.md

- 自定义的函数：

| 函数接口               | 作用                                      |
| ---------------------- | ----------------------------------------- |
| GetU(usr_name, attri); | 获取用户某属性                            |
| GetTr(tr_name, attri); | 获取宝物某属性                            |
| dump(CLT);             | 保存表格当前状态                          |
| reset(CLT);            | 清空某表（如market）                      |
| recycle(name);         | 当用户储存箱已满时，回收最低价值的宝物    |
| tomorrow();            | 时间流逝，每天刷新用户可工作/可寻宝的状态 |

- url接口函数*：

| url                                       | function              |
| ----------------------------------------- | --------------------- |
| try/<string:name>                         | login(name)；         |
| try/<string:name>/explore                 | explore(name);        |
| try/<string:name>/wear/<string:tr_name>   | wear(name,tr_name);   |
| try/<string:name>/unwear/<string:tr_name> | unwear(name,tr_name); |
| try/<string:name>/sale/<string:tr_name>   | sale(name,tr_name);   |
| try/<string:name>/unsale/<string:tr_name> | unsale(name,tr_name); |

- test函数：

| 函数接口             | 测试功能       |
| -------------------- | -------------- |
| test_work            | 赚钱           |
| test_explore         | 寻宝           |
| test_wear            | 穿戴装备       |
| test_unwear          | 脱下装备       |
| test_sale_and_unsale | 售卖、取消售卖 |
| test_buy             | 购买           |

**功能实现的具体细节见代码详细注释。*

## 表格设计（示意）

![1572240884726](C:\Users\lenovo\AppData\Roaming\Typora\typora-user-images\1572240884726.png)

## 测试结果：

1. 运行db.py创建/初始化数据库；
2. pytest自动检测test_开头的测试文件，共6个测试函数全部通过。

![image-20200115034234139](README.assets/image-20200115034234139.png)

## 一些心得体会:

1. 在这个项目中一共尝试了两种连接数据库的方式，一种是通过mongoengine，一种是flask-pymongo。个人感觉mongoengine封装程度更高，接口简洁但提供的功能没有pymongo丰富，使用上灵活性欠缺；pymongo可以实现所有的需求，但繁琐一些。
2. mongoengine在NoSQL上实现了”码“、”主码“、”外键“等功能，鉴于MongoDB（NoSQL）上并没有真正的”码“、”外键“等，可以看作是mongoengine在封装的代码中实现了同等功能，供熟悉SQL语法的用户方便地使用。在这一点上可以看出当今SQL的流行性。
3. 在进行测试的阶段，通过**pdb**的方式在测试文件中打断点调试，一度因为**[500 internal error]**的疯狂报错卡了很久，甚至怀疑数据库连接被占用；后来发现，如果要进行pdb调试，在conftest中初始化cllient时应注意开启app.testing为True。该项默认为False，若不人为开启，将无法看到所有error的具体信息，**一律报错500**！(本来很纳闷问了一圈为什么都没人遇到过这个问题，后来想想可能我的朋友们都是print()大法）
4. 事实证明虽然mongoDB支持中文，在url方式下输入中文的user name/treasure name也可以得到正确的回应，但写测试文件时最好不要直接使用中文进行query。因为在与数据库中存储的中文进行比对时，中文信息有可能匹配，也有可能不匹配；个人怀疑是编码影响，虽然所有代码文件的编码方式已统一，但我无法得知数据库存储完成后的中文信息以什么方式存在，这时候是否能正确匹配受到环境影响。