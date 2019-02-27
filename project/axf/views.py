from django.shortcuts import render,redirect

# Create your views here.

from .models import Wheel,Nav,Mustbuy,Shop,\
    Mainshows,Foodtypes,Goods,User,Carts,Order
def home(request):
    wheelList = Wheel.objects.all()
    navList = Nav.objects.all()
    mustbuyList = Mustbuy.objects.all()
    shopList = Shop.objects.all()
    shop1 = shopList[0]
    shop2 = shopList[1:3]
    shop3 = shopList[3:7]
    shop4 = shopList[7:11]

    # m = 0
    # for i in shopList:
    #     m+=1
    #     print()

    mainshowsList = Mainshows.objects.all()
    # mainshowList = mainshow[0]

    return render(request,'axf/home.html',{"title":"主页",
                                           "wheelList":wheelList,
                                           "navList":navList,
                                           "mustbuyList":mustbuyList,
                                           "shop1":shop1,"shop2":shop2,"shop3":shop3,"shop4":shop4,
                                           "mainshowsList":mainshowsList
                                           })


def market(request,categoryid,cid,sortid):
    """
    闪送超市页面
    :param request:
    :param categoryid: 分组id
    :param cid: 子组id
    :param sortid: 排序id
    :return:
    """
    leftSlider = Foodtypes.objects.all()
    if cid == '0':
        productList = Goods.objects.filter(categoryid=categoryid)
    else:
        productList = Goods.objects.filter(categoryid=categoryid,childcid = cid)

    # 排序
    if sortid == "0":  # 综合排序  为默认值
        pass
    elif sortid == "1":   # 销量排序 descend
        productList = productList.order_by("-productnum")
    elif sortid == '2': # 价格最低 ascend
        productList = productList.order_by("price")
    elif sortid == "3": # 价格最高 descend
        productList = productList.order_by("-price")

    group = leftSlider.get(typeid=categoryid)# 组id  获取一条组数据
    childList = []
    childtypename = group.childtypenames
    # 全部分类:0#进口水果:103534#国产水果:103533
    arr1 = childtypename.split("#")
    for i in arr1:
        arr2 = i.split(":")
        obj = {"childName":arr2[0],"childId":arr2[1]}
        childList.append(obj)
    print(childList)

    token = request.session.get("token")

    for product in productList:
        product.ppnum = 0
        if token:
            userInfo = User.objects.get(userToken=token)  # 根据token获取当前用户信息
            cartsList = Carts.object1.filter(userAccount=userInfo.userAccount)  # 根据用户名获取购物车信息
            for cart in cartsList:
                if product.productid == cart.productid:
                    product.ppnum = cart.productnum

    return render(request,'axf/market.html',{"title":"闪送超市",
                                             "leftSlider":leftSlider,
                                             "productList":productList,
                                             "childList":childList,
                                             "categoryid":categoryid,
                                             "cid":cid
                                             })

def cart(request):
    # 判断用户是否登录,session对话中取出token值
    token = request.session.get("token")
    cartsList = []
    if token:
        userInfo = User.objects.get(userToken=token)
        cartsList = Carts.object1.filter(userAccount=userInfo.userAccount)

    return render(request,'axf/cart.html',{"title":"购物车","cartsList":cartsList})


def changecart(request,flag):
    """
     修改购物车
    :param request: 请求体
    :param flag: 0：添加  1：删除
    :return: none
    """
    # 判断用户是否登录,session对话中取出token值
    token = request.session.get("token")
    if token == None:
        # 没有登录
        return JsonResponse({"data":"do not login","status":"error"})
    # 已经登录的条件下
    # 确认登陆后
    productid = request.POST.get("productid")   # 取出ajax-post请求发来的表单数据{producuid}
    productInfo = Goods.objects.get(productid=productid)    # 根据商品id在Goods模型中获取该商品的所有信息productInfo
    userInfo = User.objects.get(userToken=token) #  根据token获取User模型中所对应的用户数据
    if flag == "0":  # market中的增加功能“+”
        if productInfo.storenums == 0:
            return JsonResponse({"data": {"msg":"200","storenum":productInfo.storenums,
                                          "productnum":0},
                                 "status": "error"})
        else:# 对Goods中的库存进行修改
            productInfo.storenums -= 1
            productInfo.save()
        carts = Carts.object1.filter(userAccount=userInfo.userAccount)
        if carts.count() == 0:
            # 直接增加一条
            c = Carts.createcart(account=userInfo.userAccount,productid=productInfo.productid,
                                productnum=1,totalprice=productInfo.price,
                                ischose=True,productimg=productInfo.productimg,
                                productname=productInfo.productlongname,orderid="0",isdelete=False)
            c.save()
            return JsonResponse({"data": {"msg":"200","storenum":productInfo.storenums,
                                          "productnum":c.productnum,"totalprice":c.totalprice},
                                 "status": "success"})
        else:
            try: # 存在该商品  则需修改该商品数据
                one_cart = carts.get(productid=productid)
                one_cart.productnum += 1
                one_cart.totalprice = round(productInfo.price * one_cart.productnum,2)
                one_cart.save()
                return JsonResponse({"data":{"msg":"200","storenum":productInfo.storenums,
                                             "productnum":one_cart.productnum,"totalprice":one_cart.totalprice},
                                     "status": "success"})
            except Carts.DoesNotExist as e:
                c = Carts.createcart(account=userInfo.userAccount, productid=productInfo.productid,
                                    productnum=1, totalprice=productInfo.price,
                                    ischose=True, productimg=productInfo.productimg,
                                    productname=productInfo.productlongname, orderid="0", isdelete=False)
                c.save()
                return JsonResponse({"data": {"msg":"200","storenum":productInfo.storenums,
                                              "productnum":1,"totalprice":c.totalprice},
                                     "status": "success"})

    elif flag == "1":   # market中的增加功能“-”
        carts = Carts.object1.filter(userAccount=userInfo.userAccount)

        if carts.count():
            try:
                one_cart = carts.get(productid=productid)
                productInfo.storenums += 1
                productInfo.save()
                if one_cart.productnum == 1:
                    one_cart.delete()
                    return JsonResponse(
                        {"data": {"msg": "200","storenum":productInfo.storenums,
                                  "productnum":0}, "status": "success"})
                else:
                    one_cart.productnum -= 1
                    one_cart.totalprice = round(productInfo.price * one_cart.productnum,2)
                    one_cart.save()
                    return JsonResponse({"data": {"msg":"200","storenum":productInfo.storenums,
                                                  "productnum":one_cart.productnum,"totalprice":one_cart.totalprice},
                                         "status": "success"})
            except Carts.DoesNotExist as e:
                return JsonResponse({"data":{"msg":"200","storenum":productInfo.storenums,
                                             "productnum":0} , "status": "error"})
        else:
            return JsonResponse({"data": {"msg":"购物车中没有数据","storenum":productInfo.storenums,
                                          "productnum":0}, "status": "error"})


    elif flag == "2":
        # token = request.session.get("token")
        # userInfo = User.objects.get(userToken=token)
        carts = Carts.object1.filter(userAccount=userInfo.userAccount) # 取出该账户下的所有数据
        cartInfo = carts.get(productid=productid)
        str = ""
        cartInfo.ischose = not cartInfo.ischose
        if cartInfo.ischose:
            str = "√"

        cartInfo.save()
        return JsonResponse({"data":{"msg":"200",
                                     "str":str},
                             "status": "success"})


    # return render(request,'axf/cart.html',{"title":"购物车"})

def saveorder(request):

    token = request.session.get("token")
    if token == None:
        return JsonResponse({"data":{"msg":"没有登录"},"status":"error"})
    userInfo = User.objects.get(userToken=token)

    # print("ttttttttttttttttttttttttttttttttttttttttt")
    # print(userInfo.userAccount)
    # print(request.POST)

    carts = Carts.object1.filter(ischose=True)

    if carts.count() == 0:
        return JsonResponse({"data":{"msg":"没有勾选上的商品"},"status":"error"})

    oid = time.time() + random.randrange(1,100000)
    oid = "%d"%oid
    o = Order.createorder(oid,userInfo.userAccount,0)
    o.save()
    for item in carts:
        item.isDelete =  True
        item.orderid = oid
        item.save()
    return JsonResponse({"data": {}, "status": "success"})




def mine(request):

    username = request.session.get("username","未登录")

    return render(request,'axf/mine.html',{"title":"我的",
                                           "username":username})


from .forms.login import LoginForm
from django.http import HttpResponse

def login(request):
    if request.method == "POST":
        f = LoginForm(request.POST)
        if f.is_valid():
            # 信息格式没问题
            nameid = f.cleaned_data["username"]
            pswd = f.cleaned_data["passwd"]

            try:
                user = User.objects.get(userAccount=nameid)# 如果存在该用户，往下执行
                if user.userPasswd != pswd: # 账户存在，密码错误
                    return redirect('/login/')


            except User.DoesNotExist as e:# 账户不存在
                return redirect('/login/')

            # 如果上边登陆成功
            token = time.time() + random.randrange(1, 100000)
            user.userToken = str(token)
            user.save()

            request.session['username'] = user.userName  # 状态保持显示登录名
            request.session['token'] = user.userToken  # 用于登录验证

            return redirect('/mine/')
        else:
            return render(request, 'axf/login.html',
                          {'title': '登录', 'form': f, 'error': f.errors})

    else:
        f = LoginForm()
        return render(request,'axf/login.html',
                      {'title':'登录','form':f})


    # return render(request,'axf/login.html',{"title":"登录"})


# 注册
import time
import random
from django.conf import settings
import os
def register(request):
    if request.method == 'POST':
        userAccount = request.POST.get( "userAccount")
        userPasswd = request.POST.get("userPasswd")
        userName = request.POST.get("userName")
        userPhone = request.POST.get("userPhone")
        userAddress = request.POST.get("userAddress")
        # userImg =
        userRank = 0
        userToken = time.time() + random.randrange(1,100000)
        userToken = str(userToken)
        # 取上传的头像
        f = request.FILES["userImg"]
        print("*****"*50)
        print(type(request.FILES))
        print(request.FILES)
        print(request.FILES.get("userImg"))
        print(request.POST)
        userImg = os.path.join(settings.MEDIA_ROOT,userAccount + ".png") # 在服务器端创建一个图片存储地址
        with open(userImg,'wb') as fp:
            for data in f.chunks(): # chunks目的是把上传的文件分块，防止过大
                fp.write(data)  # 把图片文件写入到对应的存储地址当中
        user = User.createuser(userAccount,userPasswd,userName,userPhone,
                               userAddress,userImg,userRank,userToken)
        user.save()
        request.session['username'] = userName # 状态保持显示登录名
        request.session['token'] = userToken  # 用于登录验证
        return redirect('/mine/')
    else:
        return render(request,'axf/register.html',{'title': '注册'})

# 退出登录
from django.contrib.auth import logout
def quit(request):
    logout(request)
    return redirect('/mine/')


# 用户名验证---ajax请求
from django.http import JsonResponse
def checkuserid(request):

    userid = request.POST.get("userid")

    try:
        user = User.objects.get(userAccount=userid)
        return JsonResponse({"data":"该用户已经注册","status":"error"})
    except User.DoesNotExist as e:
        return JsonResponse({"data":"允许注册","status":"success"})


from .models import Order_d,Order_d_Goods
from django.urls import reverse
def saveorder_d(request):
    token = request.session.get('token')
    if token == None:
        return JsonResponse({'data':{'msg':'没有登录'},
                             'status':'error'})
    user = User.objects.get(userToken=token)
    if user:
        carts_goods = Carts.object1.filter(userAccount=user.userAccount,ischose=True)
        # print(type(carts_goods))
        # print(carts_goods)
        # if carts_goods.count() == 0:
        #     print("meiyou ")
        if carts_goods.count() == 0:
            return JsonResponse({"data": {"msg":'没有选商品'}, "status": "error"})
        order = Order_d.objects.create(user=user,d_status=0) #
        for carts in carts_goods:
            Order_d_Goods.objects.create(goods=Goods.objects.get(productid=carts.productid),
                                         order=order,g_num=carts.productnum)
            carts.delete()
        return JsonResponse({"data": {"order_id":order.id}, "status": "success"})
        # return redirect(reverse('axf:order_to_pay',args=(order.id,)))

def order_to_pay(request,flag):
    """
    点击选好了确认订单
    :param request:
    :return:
    """
    token = request.session.get("token")
    if token == None:
        redirect('/login/')

    user = User.objects.get(userToken=token)
    if user:
        if request.method == 'GET':
            orders = []
            if flag == "0":
                orders = Order_d.objects.filter(user=user,d_status=0) # 获取该用户所有未付款的订单
            elif flag == "1":
                orders = Order_d.objects.filter(user=user,d_status=1) # 获取该用户付款未发货的订单
            elif flag == "2":
                orders = Order_d.objects.filter(user=user,d_status=2) # 获取该用户所有付款并发货的订单
            return render(request, 'axf/order_info.html',{'orders':orders,'flag':flag})
        else:
            return HttpResponse("未登录")
    else:
        return HttpResponse("未登录")

def change_order_select(request):
    """
    注意获取request.post中传来的参数order_id
    :param request:
    :param flag:
    :return:
    """
    order_id = request.POST.get("order_id")  # 取出ajax-post请求发来的表单数据{producuid}

    token = request.session.get('token')
    if token == None:
        return JsonResponse({"data":{'msg':'没有登录'},
                             "status":"error"})

    user = User.objects.get(userToken=token) # 获取用户模型
    orders = user.order_d_set.all()# 获取该用户所有的订单
    order_des = orders.get(id=order_id)  # 获取要操作的目标订单

    str = ""
    order_des.is_select = not order_des.is_select
    if order_des.is_select:
        str = "√"
    order_des.save()
    return JsonResponse({"data": {"msg": "200",
                                  "str": str},
                         "status": "success"})



def change_order_status(request,flag):
    """
    :param request:
    :param flag:   ☆d_status：  0：下单未付款 1：付款未发货 2：付款并发货
    :return:
    """
    token = request.session.get("token")
    if token == "None":
        return JsonResponse({"data":{'msg':'没有登录'},
                             "status":"error"})
    user = User.objects.get(userToken=token)
    order_is_select = user.order_d_set.filter(d_status=0,is_select=True)

    if flag == "1":
        for item in order_is_select:
            # print("66666666666666666666")
            item.d_status = not item.d_status
            item.save()
        return JsonResponse({"data":{"msg":""},
                            "status":"success"
                            })


