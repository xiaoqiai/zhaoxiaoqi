"""
@desc: 添加订单商品
"""
from urllib import request,parse
import hashlib
import json
new_token=hashlib.md5(b'123').hexdigest()
data={'id':'5','num':3}
data = parse.urlencode(data).encode('utf8')
req=request.Request("http://127.0.0.1:5000/orders_goods/%s"%new_token,method="post",data=data)
result=request.urlopen(req)
print(result.read().decode("utf8"))