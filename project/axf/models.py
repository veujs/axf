from django.db import models

# Create your models here.
class Wheel(models.Model):
    img = models.CharField(max_length=150)
    name = models.CharField(max_length=20)
    trackid = models.CharField(max_length=20)
    # isDelete = models.BooleanField(default=False)

class Nav(models.Model):
    img = models.CharField(max_length=150)
    name = models.CharField(max_length=20)
    trackid = models.CharField(max_length=20)

class Mustbuy(models.Model):
    img = models.CharField(max_length=150)
    name = models.CharField(max_length=20)
    trackid = models.CharField(max_length=20)

class Shop(models.Model):
    img = models.CharField(max_length=150)
    name = models.CharField(max_length=20)
    trackid = models.CharField(max_length=20)

class Mainshows(models.Model):
    img = models.CharField(max_length=150)
    name = models.CharField(max_length=20)
    trackid = models.CharField(max_length=20)
    categoryid = models.CharField(max_length=20)
    brandname = models.CharField(max_length=20)

    img1 = models.CharField(max_length=150)
    childcid1 = models.CharField(max_length=20)
    productid1 = models.CharField(max_length=20)
    longname1 = models.CharField(max_length=20)
    price1 = models.CharField(max_length=20)
    marketprice1 = models.CharField(max_length=20)
    img2 = models.CharField(max_length=150)
    childcid2 = models.CharField(max_length=150)
    productid2 = models.CharField(max_length=150)
    longname2 = models.CharField(max_length=150)
    price2 = models.CharField(max_length=20)
    marketprice2 = models.CharField(max_length=20)
    img3 = models.CharField(max_length=150)
    childcid3 = models.CharField(max_length=150)
    productid3 = models.CharField(max_length=150)
    longname3 = models.CharField(max_length=150)
    price3 = models.CharField(max_length=20)
    marketprice3 = models.CharField(max_length=20)

# 分类模型
class Foodtypes(models.Model):
    typeid = models.CharField(max_length=20)
    typename = models.CharField(max_length=20)
    childtypenames = models.CharField(max_length=150)
    typesort = models.IntegerField(default=1)

# 商品信息
class Goods(models.Model):
    productid = models.CharField(max_length=16)  # 商品的id
    productimg = models.CharField(max_length=200)  # 商品的图片
    productname = models.CharField(max_length=100)  # 商品的名称
    productlongname = models.CharField(max_length=200)  # 商品的规格
    isxf = models.IntegerField(default=1)
    pmdesc = models.CharField(max_length=100)
    specifics = models.CharField(max_length=100)  # 规格
    price = models.FloatField(default=0)  # 商品的折后价格
    marketprice = models.FloatField(default=1)  # 商品的原价
    categoryid = models.CharField(max_length=16)  # 分类的id
    childcid = models.CharField(max_length=16)  # 子分类的id
    childcidname = models.CharField(max_length=100)  # 子分类的名称
    dealerid = models.CharField(max_length=16)
    storenums = models.IntegerField(default=1)  # 排序
    productnum = models.IntegerField(default=1)  # 销量排序



class User(models.Model):
    # 用户账号  唯一
    userAccount = models.CharField(max_length=20,unique=True)
    # 密码
    userPasswd = models.CharField(max_length=20)
    # 昵称
    userName = models.CharField(max_length=20)
    # 电话
    userPhone = models.CharField(max_length=20)
    # 地址
    userAddress = models.CharField(max_length=150)
    # 头像
    userImg = models.CharField(max_length=150)
    # 等级
    userRank = models.IntegerField()
    # token验证值，每次登陆之后都会更新
    userToken = models.CharField(max_length=50)

    def __str__(self):
        return self.userAccount

    # classmethod为装饰符 其对应的函数不需要实例化  要区别与类方法
    @classmethod
    def createuser(cls,account,passwd,name,phone,address,img,rank,token):
        u = cls(userAccount=account,userPasswd=passwd,userName=name,userPhone=phone,
                userAddress=address,userImg=img,userRank=rank,userToken=token)
        return u

class CartsManager1(models.Manager):
    def get_queryset(self):
        return super(CartsManager1, self).get_queryset().filter(isDelete=False)

# class CartsManager2(models.Manager):
    # def get_queryset(self):
        # return super(CartsManager2, self).get_queryset().filter(ischose=False)

class Carts(models.Model):
    # 用户id
    userAccount = models.CharField(max_length=20)
    # 商品id
    productid = models.CharField(max_length=20)
    # 数量
    productnum = models.IntegerField()
    # 总价
    totalprice = models.FloatField()
    # 是否选中
    ischose = models.BooleanField(default=True)
    # 图片
    productimg = models.CharField(max_length=150)
    # 长名字
    productlongname = models.CharField(max_length=150)
    # 属于哪个订单
    orderid = models.CharField(max_length=20,default="0")
    isDelete = models.BooleanField(default=False)


    def __str__(self):
        return self.userAccount

    object1 = CartsManager1()
    # object2 = CartsManager2()

    # classmethod为装饰符 其对应的函数不需要实例化  要区别与类方法
    @classmethod
    def createcart(cls,account,productid,productnum,totalprice,ischose,productimg,productname,orderid,isdelete):
        u = cls(userAccount=account,productid=productid,productnum=productnum,totalprice=totalprice,
                ischose=ischose,productimg=productimg,productlongname=productname,orderid = orderid,isDelete=isdelete)
        return u

class Order(models.Model):
    orderid = models.CharField(max_length=20)
    userid = models.CharField(max_length=20)
    progress = models.IntegerField()

    @classmethod
    def createorder(cls,orderid,userid,progress):
        o = cls(orderid=orderid,userid=userid,progress=progress)
        return o

class Order_d(models.Model):
    user = models.ForeignKey(User) # 关联的用户
    d_num = models.CharField(max_length=128) # 订单数量

    d_status = models.IntegerField(default=0) # 订单状态 0 下单，未付款，1 付款未发货；2 付款并发货
    d_create = models.DateTimeField(auto_now_add=True) # 订单的添加时间
    is_select = models.BooleanField(default=True) # 订单是否被选择


class Order_d_Goods(models.Model):
    goods = models.ForeignKey(Goods)
    order = models.ForeignKey(Order_d)
    g_num = models.IntegerField(default=0)





