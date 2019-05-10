"""
@desc: 添加收货地址
"""
# from urllib import request,parse
# import hashlib
# import json
# new_token=hashlib.md5(b'123').hexdigest()    #b表示字节,bytes
# data={'name':'张迪hello','phone':13849763789,'province':'陕西省','user_id':'4','city':'西安市','area':'碑林区',
#       'detail':'省体高速大厦七楼','is_default':'1'}
# data = parse.urlencode(data).encode('utf8')
# req=request.Request("http://127.0.0.1:5000/address/%s"%new_token,method="post",data=data)
# result=request.urlopen(req)
# print(result.read().decode("utf8"))

"""
@desc: 获取当前登陆用户地址信息
"""
# from urllib import request,parse
# import hashlib
# import json
# new_token=hashlib.md5(b'123').hexdigest()     #b表示字节,bytes
# data={'user_id':4}
# data = parse.urlencode(data).encode('utf8')
# req=request.Request("http://127.0.0.1:5000/address/%s"%new_token,method="get",data=data)
# result=request.urlopen(req)
# print(result.read().decode("utf8"))


"""
@desc: 用户地址修改
"""
from urllib import request,parse
import hashlib
import json
new_token=hashlib.md5(b'123').hexdigest()    #b表示字节,bytes
print(new_token)
data={'name':'小张','phone':'17836473829','province':'浙江省','id':'10','user_id':'4','city':'杭州市','area':'下沙区',
      'detail':'开心','is_default':'1'}
data = parse.urlencode(data).encode('utf8')
req=request.Request("http://127.0.0.1:5000/address/%s"%new_token,method="put",data=data)
result=request.urlopen(req)
print(result.read().decode("utf8"))