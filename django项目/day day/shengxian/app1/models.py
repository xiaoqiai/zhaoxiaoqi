from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    nick = models.CharField('昵称', max_length=10, null=True)
    avatar = models.ImageField('头像', null=True)
    tel = models.CharField('手机', max_length=11, null=True)
    sex = models.SmallIntegerField('性别', choices=((0, '女'), (1, '男'), (2, '保密')), default=2)
    birthday = models.DateField('生日', null=True)





#下拉页
class xiala(models.Model):
    class Meta:
        verbose_name = '下拉页'
        verbose_name_plural = verbose_name
    name = models.CharField('名称',max_length=20,null=True,blank=True)
    img = models.CharField('图片',max_length=20,null=True,blank=True)
    note = models.CharField('说明',max_length=20,null=True,blank=True)
    ctime = models.DateTimeField('创建时间',auto_now_add=True)
    def __str__(self):
        return self.name


#商品分类
class Good_type(models.Model):
    class Meta:
        verbose_name= '商品分类'
        verbose_name_plural = verbose_name
    name = models.CharField('图片名',max_length=20)
    note = models.CharField('说明',max_length=20)
    img = models.ImageField('图片',upload_to='picture/')
    price1 = models.FloatField('现价',null=True)
    price2 = models.FloatField('原价',null=True)
    goods_type = models.CharField('商品种类',max_length=20,null=True)
    count1 = models.IntegerField('库存量',null=True)
    count2 = models.IntegerField('销售量',null=True)
    desc = models.IntegerField('各个分类',null=True)
    ctime = models.DateTimeField('创建时间',auto_now_add=True,null=True,blank=True)
    rec = models.CharField('新品推荐',max_length=20,null=True,blank=True)
    shangjia = models.SmallIntegerField('是否上架',choices=((0,'否'),(1,'上架')),default=1)
    parent = models.ForeignKey('self',on_delete=models.CASCADE,verbose_name='父id',null=True,blank=True)
    goods = models.ManyToManyField(User, through='Cart',through_fields=('goods','user'),verbose_name='商品')
    def __str__(self):
        return self.name


#商品列表
# class Goods(models.Model):
#     class Meta:
#         verbose_name = '商品列表'
#         verbose_name_plural = verbose_name
#     name = models.CharField('名称',max_length=10)
#     title = models.CharField('标题',max_length=20)
#     price = models.IntegerField('价格',null=True,blank=True)
#     name1 = models.CharField('商品简写名称',max_length=10)
#     img1 = models.ImageField('商品图片',upload_to='picture',null=True,blank=True)#media内自动生成的文件夹
#     note = models.CharField('商品说明',max_length=100)
#     url = models.CharField('跳转地址',max_length=20,null=True,blank=True)
#     good_type = models.ForeignKey(Good_type,on_delete=models.CASCADE,verbose_name='Good_type_id',null=True,blank=True)
#     def __str__(self):
#         return self.name

#收货地址表
class Addr(models.Model):
    class Meta:
        verbose_name = '收货地址'
        verbose_name_plural = verbose_name
    name = models.CharField('收货人姓名',max_length=20,null=False)
    address = models.CharField('收货详细地址',max_length=100,null=False)
    postcode = models.CharField('邮编',max_length=20,null=False)
    tel = models.CharField('联系电话',max_length=11,null=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='用户id',null=True)
    def __str__(self):
        return self.name

#轮播图
class Banner(models.Model):
    class Meta:
        verbose_name='轮播图'
        verbose_name_plural = verbose_name
    name = models.CharField('图片名',max_length=20)
    title = models.CharField('标题',max_length=20)
    img = models.ImageField('图片',max_length=20,upload_to='picture/')
    note = models.CharField('说明',max_length=20)
    ctime = models.DateTimeField('创建时间',auto_now_add=True)
    def __str__(self):
        return self.name

#购物车
class Cart(models.Model):
    class Meta:
        verbose_name='购物车表'
        verbose_name_plural = verbose_name
    user = models.ForeignKey(User,'用户ID',null=True,blank=True)
    goods = models.ForeignKey(Good_type,'商品ID',null=True,blank=True)
    count = models.IntegerField('数量',null=True,blank=True)
    status = models.SmallIntegerField('是否启用',choices=((0,'不启用'),(1,'启用')),default=1)
    is_del = models.SmallIntegerField('是否删除',choices=((0,'不删除'),(1,'删除')),default=0)
    ctime = models.DateTimeField('创建时间',auto_now_add=True)
    # def __str__(self):
    #     return self.goods


# 订单列表
class Order_list(models.Model):
    class Meta:
        verbose_name = '订单列表'
        verbose_name_plural = verbose_name
    user_id = models.IntegerField('用户id', null=True)
    order_no=models.CharField('订单编号',null=True,max_length=100)
    is_pay = models.SmallIntegerField('支付状态', choices=((0, '未支付'), (1, '已支付')), default=0)
    ctime = models.DateTimeField('创建时间', null=True, auto_now_add=True)
    allmoney=models.CharField('总价', max_length=20, null=True)


#订单商品表
class Order_goods(models.Model):
    class Meta:
        verbose_name='订单商品表'
        verbose_name_plural=verbose_name
    user_id = models.IntegerField('用户id')
    goods_name = models.CharField('商品名称',max_length=20)
    price = models.FloatField('商品价格')
    count = models.IntegerField('商品数量')
    img = models.ImageField('商品图片')
    total = models.IntegerField('商品总价')
    is_pay = models.SmallIntegerField('是否支付',choices=((0,'未支付'),(1,'已支付')),default=0)
    pid = models.ForeignKey(Order_list,on_delete=models.CASCADE,verbose_name='订单列表')
    def __str__(self):
        return self.goods_name

























