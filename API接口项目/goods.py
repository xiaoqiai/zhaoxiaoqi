"""
@desc: 添加商品
"""
# from urllib import request,parse
# import hashlib
# import json
# new_token=hashlib.md5(b'123').hexdigest()    #b表示字节,bytes
# print(new_token)
# data={'name':'电视','img':'D://img','price':2100,'unit':'个','desc1':'质保5年，出现任何问题保修。',
#       'origin':'格力','goods_type_id':5}
# data = parse.urlencode(data).encode('utf8')
# req=request.Request("http://127.0.0.1:5000/productions/%s"%new_token,method="post",data=data)
# result=request.urlopen(req)
# print(result.read().decode("utf8"))


"""
@desc: 获取商品
"""
# from urllib import request,parse
# import hashlib
# import json
# new_token=hashlib.md5(b'123').hexdigest()    #b表示字节,bytes
# print(new_token)
# req=request.Request("http://127.0.0.1:5000/productions/%s"%new_token,method="get")
# result=request.urlopen(req)
# print(result.read().decode("utf8"))


"""
@desc: 商品修改
"""
# from urllib import request,parse
# import hashlib
# import json
# new_token=hashlib.md5(b'123').hexdigest()    #b表示字节,bytes
# print(new_token)
# data={'name':'孙尚香','img':'D://img','price':'1000','unit':'个','desc1':'品质保证，放心使用！','origin':'海尔','goods_type_id':'5',
#       'detail':'不告诉你在哪','is_default':'1'}
# data = parse.urlencode(data).encode('utf8')
# req=request.Request("http://127.0.0.1:5000/productions/%s"%new_token,method="put",data=data)
# result=request.urlopen(req)
# print(result.read().decode("utf8"))