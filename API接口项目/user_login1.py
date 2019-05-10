"""
@desc: 账号密码登录调用
"""
from urllib import request,parse
import hashlib
import json
new_token=hashlib.md5(b'123').hexdigest()   #b表示字节,bytes
data={'phone':'1872993747222','pwd':'zhaoben1018'}
data = parse.urlencode(data).encode('utf8')
req=request.Request("http://127.0.0.1:5000/user_login/%s"%new_token,method="post",data=data)
result=request.urlopen(req)
print(result.read().decode("utf8"))