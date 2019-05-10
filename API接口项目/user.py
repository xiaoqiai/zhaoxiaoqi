"""
@desc: ⽤户注册客户端调用
"""
# from urllib import request,parse
# import json
# import hashlib
# new_token= hashlib.md5(b'123').hexdigest()#拿到加密的字符串    #b表示字节,bytes
# print(new_token)
# data={'name':'小花','phone':'18973894843','pwd':'zhaoben1018'}
# data = parse.urlencode(data).encode('utf8')
# req=request.Request("http://127.0.0.1:5000/users/%s"%new_token,method="post",data=data)
# print(req)
# result=request.urlopen(req)
# print(result.read().decode("utf8"))


"""
@desc: 获取用户列表
"""
from urllib import request,parse
import hashlib
import json
new_token=hashlib.md5(b'123').hexdigest()     #b表示字节,bytes
data={'name':'zhaoben1','pwd':'zhaoben1018'}
data = parse.urlencode(data).encode('utf8')
req=request.Request("http://127.0.0.1:5000/users/%s"%new_token,method="get",data=data)
result=request.urlopen(req)
print(result.read().decode("utf8"))