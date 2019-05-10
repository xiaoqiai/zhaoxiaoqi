from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from .models import User,Addr,Banner,Good_type,xiala,Cart,Order_goods,Order_list
from .forms import RegisterForm,AddrForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist,MultipleObjectsReturned
import json
from whoosh.filedb.filestore import FileStorage
from whoosh.fields import *
from jieba.analyse import ChineseAnalyzer
from whoosh.qparser import QueryParser
from django.contrib import messages
import os
import random

def index(request):
    img=Banner.objects.filter(note=1).all()
    xiaotu = Banner.objects.filter(note=2).all()
    logo = Banner.objects.filter(note=3).all()
    zhutu = Good_type.objects.filter(desc=0).all()
    msg = Good_type.objects.filter(desc=1).all()
    if request.user.is_authenticated:
        pid = User.objects.get(username=request.user).id
        gwc = Cart.objects.filter(user_id = pid).count()
    else:
        gwc = 0

    context ={
        'img':img,
        'xiaotu': xiaotu,
        'logo': logo,
        'zhutu':zhutu,
        'msg':msg,
        'gwc':gwc

    }

    return render(request,'index.html',context)


#购物车
@login_required
#装饰器，直接跳转页面，判断是否登陆，若未登陆，跳转至登陆页面，登陆完成后直接跳转至当时点击的页面。
def cart(request):
    pid = User.objects.get(username=request.user).id
    ids = Cart.objects.filter(user_id=pid).all()
    num = Cart.objects.filter(user_id=pid).count()
    context = {
        'ids':ids,
        'num':num
    }
    return render(request,'cart.html',context)


#商品详情
def detail(request,p):
    if request.user.is_authenticated:
        #商品id
        q = Good_type.objects.get(id=p)
        #得到该商品的父id
        fu_id=q.parent_id
        #该商品父id相同的所有商品
        alls = Good_type.objects.filter(parent_id=fu_id).all()
        if request.user.is_authenticated:
            pid = User.objects.get(username=request.user).id
            gwc = Cart.objects.filter(user_id=pid).count()
        else:
            gwc = 0
        context={
            'q':q,
            'alls':alls,
            'gwc':gwc
        }
        return render(request,'detail.html',context)
    else:
        return redirect('login')

#商品详情页面跳转立即购买页面
def place_order_1(request):
    a = Addr.objects.filter(user_id=request.user.id)
    ids = request.GET.get('ids')
    ids = json.loads(ids)
    user = User.objects.filter(username=request.user).get()
    goods = Good_type.objects.filter(id=ids[0]).get()
    try:
        return render(request,'place_order.html',{'goods':goods,'count':ids[1],'ids1':ids[2],'c':ids[1],'a':a})
    except Exception:
        return render(request,'place_order.html', {'goods': goods,'a':ids[1],'ids1':ids[2],'c':ids[1]})

#用户中心——个人信息
@login_required
def user_center_info(request):
    return render(request,'user_center_info.html')

#订单信息
def order(request):
    use_id = User.objects.get(username=request.user).id
    lst = request.GET.get('order')
    lst = json.loads(lst)
    order_no = ''  #订单编号
    #自动生成6位数订单编号
    for i in range(6):
        num = random.randint(0, 9)
        num = str(num)
        order_no = order_no + num
    Order_list.objects.create(user_id=use_id,order_no = order_no) #将当前登录用户id，订单编号，存入order_list
    all_money=0
    for i in range(0,len(lst)):
        goods_name = Good_type.objects.get(id=lst[i]).name
        price = Good_type.objects.get(id=lst[i]).price1
        count = Good_type.objects.get(id=lst[i]).count1
        img = Good_type.objects.get(id=lst[i]).img
        pid = Order_list.objects.get(order_no = order_no).id
        Order_goods.objects.create(
            user_id=use_id, goods_name=goods_name, price=price, count=count,img=img,total=count*price,pid_id = pid
        )
        total = count * price
        all_money+=total
    Order_list.objects.filter(order_no=order_no).update(allmoney=all_money,is_pay=1)
    return redirect('user_center_order')


#用户中心——我的订单
@login_required
def user_center_order(request):
    order_lst = Order_list.objects.filter(user_id=request.user.id)  # 得到order_list表中所有内容
    order_good = Order_goods.objects.filter(user_id=request.user.id)
    context = {
        'order_lst':order_lst,
        'order_good':order_good
    }
    return render(request,'user_center_order.html',context)


#提交订单
def place_order(request):
    a = Addr.objects.filter(user_id=request.user.id)
    use_id = User.objects.get(username=request.user).id  #当前登录用户id
    try:
        c = request.GET.get('ids')
        b = json.loads(c)
        order = Cart.objects.filter(goods_id__in=b)
        num = Cart.objects.filter(user_id=use_id).count()
    except Exception:
        order = Cart.objects.filter(user_id=use_id).all()
        num = Cart.objects.filter(user_id=use_id).count()
    context = {
        'a': a,
        'order': order,
        'num':num
    }
    return render(request, 'place_order.html', context)

#购物车数量变化，在cart页面加减数量，同时在表中更新数量（有异常）
def car_count(request):
    goods_id = json.loads(request.GET.get('v1'))
    count = json.loads(request.GET.get('v2'))
    for i in range(0, len(count)):
        Cart.objects.filter(goods_id=goods_id[i]).update(count=count[i])
    return redirect('place_order')

#商品列表
def list(request,p,b=1):
    new_rec = Good_type.objects.filter(parent_id = p).all()
    fu_id = Good_type.objects.filter(desc=0).get(id=p)
    paginator = Paginator(new_rec,3)
    page = paginator.get_page(b)
    if request.user.is_authenticated:
        pid = User.objects.get(username=request.user).id
        gwc = Cart.objects.filter(user_id = pid).count()
    else:
        gwc = 0
    context={
        'new_rec':new_rec,
        'fu_id':fu_id,
        'page':page,
        'gwc':gwc
    }
    return render(request,'list.html',context)

#收货地址
def addr(request):
    #判断用户是否登陆
    if request.user.is_authenticated:
        #判断是否是post请求
        if request.method == 'POST':
            #获取输入内容
            name = request.POST.get('name')
            address = request.POST.get('address')
            postcode = request.POST.get('postcode')
            tel = request.POST.get('tel')
            #判断各字段不为空，执行添加
            if name!='' and address != '' and postcode != '' and tel != '':
                #获取当前登录用户id
                z=request.user
                b=User.objects.get(username=z)
                pid = User.objects.get(username=b).id
                add = Addr.objects.create(name=name,address=address,postcode=postcode,tel=tel,user_id=pid)
                if add is not None:
                    res = {'na':'添加成功'}
                    return JsonResponse(res)
                else:
                    res = {'na' :'添加失败'}
                    return JsonResponse(res)
            else:
                return JsonResponse({'na': '提示：字段不能为空'})
        else:
            a = Addr.objects.filter(user_id=request.user.id)
            context = {
                'a':a
            }
            return render(request,'user_center_site.html',context)
    else:
        return redirect('login')

#form 方法添加收货地址
# def addr(request):
#     if request.method == 'POST':
#         print(1)
#         form = AddrForm(request.POST)
#         print(3)
#         if form.is_valid():
#             print(2)
#             name = request.POST.get('name')
#             address = request.POST.get('address')
#             postcode = request.POST.get('postcode')
#             tel = request.POST.get('tel')
#             login_name = request.user.username
#             pid = User.objects.get(username = login_name).id
#             name_addr = Addr.objects.create(name=name,address=address,postcode=postcode,tel=tel)
#             print(pid)
#             addr = Addr.objects.filter(user_id = request.user.id).last()
#             context = {'addr':addr}
#             return render(request,'user_center_site.html',context)
#     else:
#         form = AddrForm()
#         print(5)
#     context1 = {'form':form}
#     print(4)
#     addr = Addr.objects.filter(user_id = request.user.id).last()
#     context = {'addr':'addr'}
#     return render(request,'user_center_site.html',context1,context)

#注册
def register(request):
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        email=request.POST.get('email')
        if form.is_valid():
            a=form.save()
            user_email=User.objects.filter(username=a).update(email=email)
            return redirect('login')
    else:
        form = RegisterForm()

    context = {
        'form': form
    }
    return render(request, 'register.html', context)

#登录
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request,data=request.POST)
        if form.is_valid():
            #获取当前登录的用户对象
            user = form.get_user()
            #登陆成功需要把当前用户存储下来
            #django.contrib.auth.login 函数用于将指定用户对象添加为 request.user 属性
            auth_login(request,user=user)
            # auth_login(request,email=email)
            return redirect(request.POST.get('next','index'))
    else:
        form = AuthenticationForm()
    context = {
        'form':form,
        'next':request.GET.get('next','index')
    }
    return render(request,'login.html',context)


#退出注册
def logout(request):
    auth_logout(request)
    return redirect('index')

#轮播图
def banner(request):
    img=Banner.objects.filter(note=1).all()
    context ={
        'img':img
    }
    return render(request,'index.html',context)


# #注册(me)
# def do_register(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         pwd = request.POST.get('pwd')
#         cpwd = request.POST.get('cpwd')
#         email = request.POST.get('email')
#         try:
#             check = User.objects.get(name=name)
#         except ObjectDoesNotExist:
#             if name and pwd == cpwd and pwd:
#                 User.objects.create(name=name, pwd=pwd, email=email)
#                 res = {'name':'添加成功,请点击登录！'}
#             else:
#                 res = {'name':'添加失败'}
#             return JsonResponse(res)
#         return JsonResponse({'name':'用户已存在'})
#     else:
#         return render(request,'register.html')


#登录1(正确)
# def do_login(request):
#     if request.method == 'POST':
#         user_name = request.POST.get('name')
#         pwd = request.POST.get('pwd')
#         try:
#             check = User.objects.get(name=user_name)
#         except ObjectDoesNotExist:
#             return HttpResponse('用户名不存在')
#         if check.pwd == pwd:
#             return HttpResponse('登陆成功')
#         else:
#             return HttpResponse('登录失败')
#     else:
#         return render(request,'login.html')
#
#加入购物车
def adds(request,good_id):
    use = User.objects.get(username=request.user)
    add = Cart.objects.create(user_id=use.id,goods_id=good_id,count=1)
    shangpin = Good_type.objects.get(id=good_id)
    q=shangpin.parent_id
    return redirect('/app1/list/'+str(q))

#购物车删除
def dele(request,p):
    Cart.objects.filter(id=p).delete()
    return redirect('cart')

#创建索引
def create_index(request):
    analyzer = ChineseAnalyzer()
    schema = Schema(
        name = TEXT(stored=True,analyzer=analyzer),
        datail = TEXT(stored=True,analyzer=analyzer),
        ids = TEXT(stored=True)
    )
    file_storage = FileStorage('./index')
    if not os.path.exists('./index'):
        os.mkdir('./index')
        ix = file_storage.create_index(schema)
    else:
        ix = file_storage.open_index()
    writer = ix.writer()
    for goods in Good_type.objects.all():
        writer.add_document(name=goods.name,datail = goods.note,ids=str(goods.id))
    writer.commit()
    return HttpResponse('索引创建完成')

#全文检索
def search(request):
    keywords = request.GET.get('keywords')
    file_storage = FileStorage('./index')
    ix = file_storage.open_index()
    with ix.searcher() as searcher:
        # 创建query对象，被用来搜索的
        # QueryParser(检索的字段名, 索引结构).parse(关键词)
        query = QueryParser('name',ix.schema).parse(keywords)
        # limit限制搜索结果的条数，默认为10个，指定为None则显示所有
        results = searcher.search(query,limit=None)
        lst=[]
        for res in results:
            lst.append(int(res.get('ids')))
        #当前lst中商品所有信息（lst中是符合当前搜索条件的商品id）
        if lst:
            suoyou=Good_type.objects.filter(id__in=lst).all()
        else:
            suoyou = Good_type.objects.filter(desc=1,name__contains=keywords)
        context = {
            'new_rec': suoyou
        }
        return render(request, 'list.html', context)

        # else:
        #     messages.success(request,'没有商品信息')
        #     return redirect('index')




