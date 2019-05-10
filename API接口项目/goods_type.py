"""
@desc: 添加商品分类
"""
from urllib import request,parse
import hashlib
import json
new_token=hashlib.md5(b'123').hexdigest()
data={'name':'电冰箱','img':'D://img','pid':5}
data = parse.urlencode(data).encode('utf8')
req=request.Request("http://127.0.0.1:5000/product_classes/%s"%new_token,method="post",data=data)
result=request.urlopen(req)
print(result.read().decode("utf8"))



"""
@desc: 获取商品分类
"""
# from urllib import request,parse
# import hashlib
# import json
# new_token=hashlib.md5(b'123').hexdigest()    #b表示字节,bytes
# # data={'name':'冰箱','img':'D://img','price':2600,'unit':'个','desc':'冰箱质保5年，出现任何问题保修。',
# #       'origin':'格力','goods_type_id':5}
# # data = parse.urlencode(data).encode('utf8')
# admin_user_id=1
# req=request.Request("http://127.0.0.1:5000/product_classes/%s"%admin_user_id,method="get")
# result=request.urlopen(req)
# print(result.read().decode("utf8"))