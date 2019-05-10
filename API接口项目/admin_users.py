"""
@desc: 添加管理员用户 客户端调用
"""
# from urllib import request,parse
# import json
# import hashlib
# new_token= hashlib.md5(b'123').hexdigest()#拿到加密的字符串     #b表示字节,bytes
# data={'name':'小赵','phone':'14919491479','pwd':'zhaoben1018'}
# data = parse.urlencode(data).encode('utf8')
# req=request.Request("http://127.0.0.1:5000/admin_users/%s"%new_token,method="post",data=data)
# print(req)
# result=request.urlopen(req)
# print(result.read().decode("utf8"))

"""
@desc: 获取管理员用户列表
"""
# from urllib import request,parse
# import json
# import hashlib
#
# new_token= hashlib.md5(b'123').hexdigest()#拿到加密的字符串    #b表示字节,bytes
# # data={'name':'zhaoben1','pwd':'zhaoben1018'}
# # data = parse.urlencode(data).encode('utf8')
# req=request.Request("http://127.0.0.1:5000/admin_users/%s"%new_token,method="get")
# result=request.urlopen(req)
# print(result.read().decode("utf8"))


"""
@desc: 更新管理员用户信息，编辑管理员账号和权限
"""
from urllib import request,parse
import hashlib
import json
new_token=hashlib.md5(b'123').hexdigest()    #b表示字节,bytes
print(new_token)
data={'id':2,'user_id':4}
data = parse.urlencode(data).encode('utf8')
req=request.Request("http://127.0.0.1:5000/admin_users/%s"%new_token,method="put",data=data)
result=request.urlopen(req)
print(result.read().decode("utf8"))


