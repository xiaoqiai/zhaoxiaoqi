"""
@desc: 获取订单用户列表
"""
# from urllib import request,parse
# import hashlib
# import json
# new_token=hashlib.md5(b'123').hexdigest()
# data={'user_id':'4'}
# data = parse.urlencode(data).encode('utf8')
# req=request.Request("http://127.0.0.1:5000/orders/%s"%new_token,method="get",data=data)
# result=request.urlopen(req)
# print(result.read().decode("utf8"))


"""
@desc: 改变订单状态
"""
from urllib import request,parse
import hashlib
new_token=hashlib.md5(b'123').hexdigest()    #b表示字节,bytes
print(new_token)
data={'id':2}
data = parse.urlencode(data).encode('utf8')
req=request.Request("http://127.0.0.1:5000/orders/%s"%new_token,method="put",data=data)
result=request.urlopen(req)
print(result.read().decode("utf8"))
