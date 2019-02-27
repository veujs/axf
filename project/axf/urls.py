from django.conf.urls import url
# from django.contrib import admin
from . import views


urlpatterns = [
    url(r'^home/$',views.home, name='home'),
    url(r'^market/(\d+)/(\d+)/(\d+)/$', views.market, name='market'),
    url(r'^cart/$', views.cart, name='cart'),
    url(r'^mine/$', views.mine, name='mine'),

    # 修改购物车
    url(r'^changecart/(\d+)/$', views.changecart, name='changecart'),
    url(r'^saveorder/$', views.saveorder, name='saveorder'),



    url(r'^login/$',views.login, name='login'),
    url(r'^register/$',views.register, name='register'),
    url(r'^quit/$', views.quit,name='quit'),
    # 验证
    url(r'^checkuserid/$', views.checkuserid, name='checkuserid'),

    # order订单新添加  wzp
    url(r'^saveorder_d/$', views.saveorder_d, name='saveorder_d'),
   # order订单付款页面  wzp
    url(r'^order-to-pay/(\d+)/$', views.order_to_pay, name='order_to_pay'),
    # 是否勾选该订单
    url(r'^change-order-select/$', views.change_order_select, name='change_order_select'),
    # 确认修改订单的状态
    url(r'^change-order-status/(\d+)/$',views.change_order_status,name='change_order_status')



]



