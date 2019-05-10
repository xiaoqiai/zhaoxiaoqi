import pymysql
from flask import Flask,jsonify
from flask_restful import reqparse,abort,Api,Resource
import re,hashlib
import time  #获取当前时间
from MysqlHelper import *


# now_time=datetime.datetime.now()
now_time=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))    #获取当前时间

app=Flask(__name__)
api=Api(app)
#定义装饰器，用来验证token，默认token为123，可以修改，也可是使用加密方式进行加密处理
#所有的链接后边都要加上123，不然就会报错。
def checkToken(func):  #func是接收需要装饰的函数名
    def handle_args(*args,**kwargs):  #args是接收需要装饰的函数内的参数，处理传入函数的参数
        #这里的123是自己加的验证码，你可以使用MD5函数或别的方法加密，保证接口安全
        print(1)
        if kwargs['token']!=hashlib.md5(b'123').hexdigest():
            abort(401,message='请带入正确的token')
        else:
            return func(*args,**kwargs)   #函数调用
    return handle_args

def rule(func):                    #权限装饰器，根据路由传过来的管理员用户id，来查询这个用户是否有此类操作的权限。
    def handle_args(*args,**kwargs):
        user_id=kwargs['admin_user_id']
            #管理员用户id
        sql='select r.action from admin_users as a inner JOIN post as p on a.post_id=p.id inner join post_rule as pr on p.id=pr.post_id inner join rule as r on pr.rule_id=r.id where a.id=%s'
        mq=connect()     #数据库实例化
        mq.cursor.execute(sql,user_id)
        val =mq.cursor.fetchall()[0]
        if func.__name__==val['action']:
            return func(*args,**kwargs)
        else:
            result={}
            result['code']=1050
            result['msg']='没有操作权限'
            return jsonify(result)
    return handle_args



#Flask-RESTful提供了一个用于参数解析的RequestParser类，类似于python中自带的argparse类，可以很方便的解析请求中的-d参数，并进行类型转换。
parser=reqparse.RequestParser()
parser.add_argument('id')          #当前id
parser.add_argument('user_id')     #当前登录用户id
parser.add_argument('name')        #名称
parser.add_argument('phone')       #电话
parser.add_argument('pwd')         #密码
parser.add_argument('province')    #省份
parser.add_argument('city')        #城市
parser.add_argument('area')        #区域
parser.add_argument('detail')      #详情
parser.add_argument('img')         #图片
parser.add_argument('pid')         #父id
parser.add_argument('price')       #价格
parser.add_argument('unit')        #单位
parser.add_argument('desc1')        #简介
parser.add_argument('origin')      #品牌
parser.add_argument('goods_type_id')
parser.add_argument('num')
parser.add_argument('post_id')
#我们观察标准的API接口，这里的接口可以分为两类：带有item_id的，和不带有item_id的。前者是操作单一资源，后者是操作资源列表或新建一个资源

#用户注册
#post /api/users
class users(Resource):
    @checkToken  #装饰器，Token令牌，检测用户身份验证
    def post(self,token):
        args=parser.parse_args()  #返回规定格式的数据，接收所有参数
        result={}
        result['code']=0
        # 这里写插入数据库逻辑，然后将id返回给下边data中的id
        if args['name'] == '':
            result['code']=403
            result['msg']='用户名不能为空'
            return jsonify(result)
        elif args['phone'] == '':
            result['code']=403
            result['msg']='电话号码不能为空'
            return jsonify(result)
        elif re.match(r"^1[35678]\d{9}$",args['phone']) is None:
            result['code']=1000
            result['msg']='电话号码格式不正确'
            return jsonify(result)
        elif args['pwd'] == '':
            result['code']=403
            result['msg']='密码不能为空'
            return jsonify(result)
        #这里写数据库逻辑
        mq = connect()  # 数据库函数实例化
        sql1 = 'select phone from user where phone=%s'  #查询已存在的电话，和当前注册用户名比较，判断电话是否存在。
        phone1 = args['phone']                          #args['phone']这个是当前输入的电话
        a = mq.cursor.execute(sql1, phone1)
        print(a)
        if a:  # 当a不等于0是表示数据库已存在该用户名，当a等于0时表示没有该用户，可以继续添加。
            result['code'] = 1001
            result['msg'] = '此号码已存在'
            return jsonify(result)
        else:
            # mysqlHelper=MysqlHelper('localhost',3306,'api_project','xiaoqi','zhaoben1018','utf8')
            sql = 'insert into user(name,phone,pwd,create_time) values(%s,%s,%s,%s)'
            params = [args['name'],args['phone'],args['pwd'],now_time]
            # count = mysqlHelper.insert(sql,params)
            mq.cursor.execute(sql,params)
            new_id=mq.cursor.lastrowid          #获取当前新增用户id
            # 这里写插入数据库逻辑，然后将id返回给下边data中的id
            result['data']={'user':{'id':new_id,'name':args['name'],'phone':args['phone'],'pwd':args['pwd'],'create_time':now_time}}
            return jsonify(result)

#GET /api/users 获取用户列表
    @checkToken
    def get(self,token):
        args=parser.parse_args()  #以规定格式返回数据，接收所有参数
        result={}
        result['code']=0
        if args['name']=='' and args['pwd']=='':   #判断不能为空
            result['code']=403
            result['msg']='用户名和密码不能为空'
            return jsonify(result)
        else:
            mq = connect()      #数据库类实例化
            names=args['name']
            sql1='select pwd from admin_users where name=%s'  #根据输入的用户名得到密码
            a1=mq.cursor.execute(sql1,names)
            if a1:                      #如果用户名存在，则为真，下面继续判断密码是否相等
                passwd = mq.cursor.fetchall()[0]['pwd']  # 得到数据库中已存在的密码
                if args['pwd']==passwd:
                    sql='select * from user'        #拿到user表中所有内容
                    a=mq.cursor.execute(sql)
                    all_value=mq.cursor.fetchall()   #得到是一个列表套字典
                    if a:
                        result['code']=200
                        result['data']={'user':all_value}   #直接将得到的列表传进去，all_value
                        return jsonify(result)

                    else:
                        result['code']=1010
                        result['msg']='获取用户列表失败'
                        return jsonify(result)
                else:
                    result['code']=1003
                    result['msg']='密码输入错误'
                    return jsonify(result)



# POST /api/user_login/{param} 账号密码登录
class login_users(Resource):
    @checkToken
    def post(self, token):
        args = parser.parse_args()   # 返回规定格式的数据
        result = {}
        result['code'] = 0            # 这里的data值是你从数据库里根据提交过来的phone和pwd进行查询而得到的值，你可以加上容错判断# 如果找不到，则用函数abort()返回错误
        if args['phone']=='' and args['pwd']=='':
            result['code']=403
            result['msg']='电话或密码不能为空'
            return jsonify(result)
        else:
            mq=connect()
            phone1=args['phone']
            sql='select pwd from user where phone=%s'
            a=mq.cursor.execute(sql,phone1)

            if a:
                passwd = mq.cursor.fetchall()[0]['pwd']
                if passwd==args['pwd']:  #fetchall得到的是元组套元组
                    result['code']=200
                    result['msg']='登陆成功'
                    return jsonify(result)
                else:
                    result['code'] = 1003
                    result['msg'] = '密码输入错误'
                    return jsonify(result)
            else:
                result['code'] = 1002
                result['msg'] = '此号码不存在'
                return jsonify(result)
        result['data'] = {'user_id': 'user_id'}
        return jsonify(result)



# POST /api/address 用户地址添加
class address(Resource):
    @checkToken
    def post(self,token):
        args=parser.parse_args()
        result={}
        result['code']=0
        login_id=args['user_id']  #当前登录用户id
        if args['province']=='' or args['city']=='' or args['area']=='' or args['detail']=='' or args['name']=='' or args['phone']=='':
            result['code']=403
            result['msg']='地址各项不能为空'
            return jsonify(result)
        elif re.match(r"^1[35678]\d{9}$",args['phone']) is None:
            result['code']=1000
            result['msg']='电话号码格式不正确'
            return jsonify(result)
        else:
            mq = connect()  # 进行类实例化
            sql='insert into addr values(null,%s,%s,%s,%s,%s,%s,%s,%s,%s,null)'
            params=[args['name'],args['phone'],args['province'],args['city'],args['area'],args['detail'],login_id,False,now_time]
            return_value=mq.cursor.execute(sql,params)
            if return_value:
                result['code']=200
                result['msg']='地址添加成功'
                result['data'] = {'addr': {'user_id': login_id, 'name': args['name'], 'phone': args['phone'],
                                           'desc':{'province': args['province'],'city': args['city'], 'area': args['area'], 'detail': args['detail'],'is_deafult': False, 'create_time': now_time}}}
                return jsonify(result)
            else:
                result['code']=1020
                result['msg']='地址添加失败，请祥查原因！'
                return jsonify(result)

#GET /api/address?user_id 用户地址获取
    @checkToken
    def get(self,token):
        args=parser.parse_args()
        result={}
        result['code']=0
        mq = connect()
        ids=args['user_id']
        sql='select * from addr where user_id=%s'
        a=mq.cursor.execute(sql,ids)
        print(a,111111)
        all_value=mq.cursor.fetchall()
        if a:
            result['code']=200
            result['data']={'user_id':args['user_id'],'address':all_value}
            return jsonify(result)
        else:
            result['code']=1002
            result['msg']='该用户id不存在'
            return jsonify(result)


#PUT /api/address/{address_id} 用户地址修改
    @checkToken
    def put(self,token):
        args=parser.parse_args()
        result={}
        result['code']=0
        if re.match(r"^1[35678]\d{9}$",args['phone']) is None:
            result['code']=1000
            result['msg']='电话号码格式不正确'
            return jsonify(result)
        else:
            mq = connect()  # 进行类实例化
            sql = 'update addr set name=%s,phone=%s,province=%s,city=%s,area=%s,detail=%s,is_default=%s,update_time=%s where id=%s'
            params = [args['name'], args['phone'], args['province'], args['city'], args['area'], args['detail'],
                      False, now_time,args['id']]
            return_value = mq.cursor.execute(sql, params)
            if return_value:
                result['code'] = 200
                result['msg'] = '地址更新成功'
                result['data'] = {'addr': {'user_id': args['user_id'], 'name': args['name'], 'phone': args['phone'],
                                           'desc': {'province': args['province'], 'city': args['city'],
                                                    'area': args['area'], 'detail': args['detail'], 'is_deafult': False,
                                                    'update_time': now_time}}}
                return jsonify(result)
            else:
                result['code'] = 1020
                result['msg'] = '地址更新失败，请祥查原因！'
                return jsonify(result)




#POST /api/admin_users 添加管理员用户
class admin_users(Resource):
    @checkToken
    def post(self,token):
        args=parser.parse_args()
        result={}
        result['code']=0
        if args['name']=='' or args['phone']=='' or args['pwd']=='':
            result['code']=403
            result['msg']='请填写您完整的信息'
            return jsonify(result)
        mq=connect()
        sql1='select name from admin_users where name=%s'
        params1=args['name']
        a1=mq.cursor.execute(sql1,params1)
        if a1:
            result['code']=1001
            result['msg']='该用户名已存在！'
            return jsonify(result)
        else:
            sql='insert into admin_users values(null,%s,%s,%s,%s,null,null,%s,null)'
            params=[args['name'],args['phone'],args['pwd'],False,now_time]
            a=mq.cursor.execute(sql,params)
            new_id=mq.cursor.lastrowid             #获取当前新增用户id
            result['data'] = {'admin_users': {'id': new_id, 'name': args['name'], 'phone': args['phone'], 'pwd': args['pwd'],
                                       'is_super':False,'create_time': now_time}}
            return jsonify(result)

#GET /api/admin_users 获取管理⽤户列表       #用这个地址访问  http://127.0.0.1:5000/get_admin_list/202cb962ac59075b964b07152d234b70
    @checkToken
    def get(self,token):
        result={}
        result['code']=0
        mq=connect()
        sql='select * from admin_users'
        a=mq.cursor.execute(sql)
        req=mq.cursor.fetchall()
        if a:
            result['code']=200
            result['data']={'get_admin_list':req}
            return jsonify(result)


#PUT /api/admin_ users/{Admin_id} 更新管理员用户信息
#编辑管理员账号和权限

    @checkToken
    def put(self,token):
        args= parser.parse_args()
        result={}
        result['code']=0
        mq=connect()
        sql='select is_super from admin_users where id=%s'%args['id']
        mq.cursor.execute(sql)
        req=mq.cursor.fetchall()[0]['is_super']
        print(req,2222222)
        if req==1:
            sql1='update admin_users set is_super=1 where id=%s'%args['user_id']
            mq.cursor.execute(sql1)
            sql2='select * from admin_users where id=%s'%args['user_id']
            mq.cursor.execute(sql2)
            req2=mq.cursor.fetchall()
            result['code']=200
            result['data']={'admin_user':req2}
            return jsonify(result)
        else:
            result['code']=1050
            result['msg']='没有操作权限'
            return jsonify(result)



#POST /api/product_classes 添加商品分类
class product_classes(Resource):
    @checkToken
    def post(self,token):
        args=parser.parse_args()
        result={}
        result['code']=0
        if args['name'] and args['img']:
            print(args['img'])
            mq=connect()
            sql='insert into goods_type values(null,%s,%s,%s,%s)'
            params=[args['name'],args['img'],now_time,args['pid']]
            a=mq.cursor.execute(sql,params)
            new_id = mq.cursor.lastrowid  # 获取当前新增用户id
            if a:
                result['code']=200
                result['data']={'add_goods_type':{'id':new_id,'name':args['name'],'img':args['img'],'create_time':now_time,'pid':args['pid']}}
                return jsonify(result)
            else:
                result['code']=1030
                result['msg']='商品分类添加失败！'
                return jsonify(result)
        else:
            result['code']=403
            result['msg']='商品分类名或图片不能为空！'
            return jsonify(result)

#GET /api/product_classes 获取商品分类  #用这个地址访问  http://127.0.0.1:5000/get_goods_type_list/202cb962ac59075b964b07152d234b70
    @rule
    def get(self,admin_user_id):
        result={}
        result['code']=0
        mq=connect()
        sql='select * from goods_type'
        a=mq.cursor.execute(sql)
        req=mq.cursor.fetchall()
        if a:
            result['code']=200
            result['data']={'get_goods_type_list':req}
            return jsonify(result)



#POST /api/productions 添加商品
class productions(Resource):
    @checkToken
    def post(self,token):
        args=parser.parse_args()
        result={}
        result['code']=0
        if args['name'] and args['img'] and args['price'] and args['origin'] and args['goods_type_id']:
            mq=connect()
            sql='insert into goods values(null,%s,%s,%s,%s,%s,%s,%s,%s,null)'
            params=[args['name'],args['img'],args['price'],args['unit'],args['desc1'],args['origin'],args['goods_type_id'],now_time]
            a=mq.cursor.execute(sql,params)
            new_id=mq.cursor.lastrowid
            if a:
                result['code']=200
                result['data']={'id':new_id,'name':args['name'],'img':args['img'],'price':args['price'],
                                'unit':args['unit'],'desc':args['desc1'],'origin':args['origin'],
                                'goods_type_id':args['goods_type_id'],'create_time':now_time}
                return jsonify(result)
            else:
                result['code']=1040
                result['msg']='商品添加失败！'
                return jsonify(result)
        else:
            result['code']=403
            result['msg']='请填写完整您的数据！'
            return jsonify(result)

#GET /api/productions 获取商品
    @checkToken
    def get(self,token):
        result={}
        result['code']=0
        mq=connect()
        sql="select * from goods"
        a=mq.cursor.execute(sql)
        if a:
            req=mq.cursor.fetchall()
            result['code']=200
            result['data']={'productions':req}
            return jsonify(result)

#PUT /api/productions/{prod_id} 修改商品
    @checkToken
    def put(self,token):
        args=parser.parse_args()
        result={}
        result['code']=0
        mq=connect()
        sql='update goods set name=%s,img=%s,price=%s,unit=%s,desc1=%s,origin=%s,goods_type_id=%s,update_time=%s where id=%s'
        params=[args['name'],args['img'],args['price'],args['unit'],args['desc1'],args['origin'],
                args['goods_type_id'],now_time,3]
        a=mq.cursor.execute(sql,params)

        if a:
            result['code']=200
            result['data']={'id':3,'name':args['name'],'img':args['img'],'price':args['price'],'unit':args['unit'],
                            'desc':args['desc1'],'origin':args['origin'],'goods_type_id':args['goods_type_id'],'update_time':now_time}
            return jsonify(result)

#POST  添加订单商品
class orders_goods(Resource):
    @checkToken
    def post(self,token):
        args=parser.parse_args()
        result={}
        result['code']=0
        mq=connect()
        sql='select * from goods where id=%s'%(args['id'])
        mq.cursor.execute(sql)
        req=mq.cursor.fetchall()[0]
        goods_name=req['name']
        price=req['price']
        img=req['img']
        total=int(req['price'])*int(args['num'])   #小计
        sql1='insert into order_detail values(null,%s,%s,%s,%s,%s,%s)'
        params=[goods_name,price,args['num'],img,total,args['id']]
        a=mq.cursor.execute(sql1,params)
        if a:
            result['code']=200
            result['data']={'orders':{'goods_name':goods_name,'price':price,'num':args['num'],'img':img,
                                      'total':total,'goods_id':args['id']}}
            return jsonify(result)


#GET /api/orders?user_id 获取⽤户订单列表
class orders(Resource):
    @checkToken
    def get(self,token):
        args=parser.parse_args()
        result={}
        result['code']=0
        mq=connect()
        sql = 'select id from `order` where user_id=%s'%(args['user_id'])    #order是Python中的关键字
        a=mq.cursor.execute(sql)
        if a:
            req=mq.cursor.fetchall()
            id_lst=[]
            for i in req:
                s=i['id']
                id_lst.append(s)
            print(id_lst)
            sql1='select * from order_detail where order_id=%s'
            goods_lst=[]
            for i in id_lst:
                params1=i
                a1=mq.cursor.execute(sql1,params1)
                req1=mq.cursor.fetchall()
                goods_lst.append(req1)
                if a1:
                    result['code']=200
                    result['data']={'orders':goods_lst}
            return jsonify(result)

#PUT /api/orders/{order_id} 改变订单状态
    @checkToken
    def put(self,token):
        args=parser.parse_args()
        result={}
        result['code']=0
        mq=connect()
        sql='update `order` set status=1 where id=%s'%(args['id'])
        mq.cursor.execute(sql)
        sql1='select * from `order` where id=%s'%(args['id'])
        a=mq.cursor.execute(sql1)
        req=mq.cursor.fetchall()
        print(req)
        if a:
            result['code']=200
            result['data']={'status':req}
            return jsonify(result)





api.add_resource(users, '/users/<token>')                            #用户
api.add_resource(login_users, '/user_login/<token>')                 #用户登录
api.add_resource(admin_users, '/admin_users/<token>')                #管理员用户
api.add_resource(address, '/address/<token>')                        #地址
api.add_resource(product_classes, '/product_classes/<token>')        #商品分类
api.add_resource(productions, '/productions/<token>')                #商品
api.add_resource(orders_goods,'/orders_goods/<token>')               #订单商品
# api.add_resource(product_classes,'/product_classes/<admin_user_id>')      #商品分类
api.add_resource(orders, '/orders/<token>')
if __name__=='__main__':
    app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))
    app.config['JSON_AS_ASCII'] = False
    #设置显示内容为字符串，而不是字节码。
    app.run(debug=True)


