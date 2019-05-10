from django.urls import path
from . import views

urlpatterns = [
    path('index/',views.index,name='index'),
    path('cart/',views.cart,name='cart'),
    path('login/',views.login,name='login'),
    #加入购物车
    path('adds/<int:good_id>',views.adds,name='adds'),
    path('register/',views.register,name='register'),
    path('user_center_info/',views.user_center_info,name='user_center_info'),
    #商品详情
    path('detail/<int:p>',views.detail,name='detail'),
    path('user_center_order/',views.user_center_order,name='user_center_order'),
    #订单信息
    path('order/',views.order,name='order'),
    path('place_order/', views.place_order, name='place_order'),
    path('list/<int:p>',views.list,name='list'),
    path('list/<int:p>?<int:b>',views.list,name='list'),

    #收货地址
    path('addr/',views.addr,name='addr'),
    #退出登录
    path('logout/',views.logout,name='logout'),
    #轮播图
    path('banner/',views.banner,name='banner'),
    #购物车页面删除
    path('dele/<int:p>',views.dele,name='dele'),
    #购物车数量变化
    path('car_count/',views.car_count,name='car_count'),
    #商品详情页面跳转立即购买页面
    path('place_order_1/',views.place_order_1,name='place_order_1'),
    #创建索引
    path('create_index/',views.create_index,name='create_index'),
    #全文检索
    path('search/',views.search,name='search'),
]