

$(document).ready(function(){

    //添加购物车
    var subShoppings=document.getElementsByClassName("subShopping");
    var addShoppings = document.getElementsByClassName("addShopping");

    console.log(addShoppings.length);
    for( i = 0; i < addShoppings.length; i++){
        addShopping = addShoppings[i];

        addShopping.addEventListener("click",function(){
            proid = this.getAttribute("ga");
            $.post("/changecart/0/",{"productid":proid},function(data)
            {
                if(data.status === "success"){
                    //添加成功，吧中间的span的innetHTML变成当前的数量

                    document.getElementById(proid + "num").innerHTML=data.data["productnum"];
                    console.log("++++++++++++++++++++++++++++++++++++++++++");
                    document.getElementById(proid + "price").innerHTML = data.data.totalprice;
                }
            })

        })
    }
    for(i = 0; i < subShoppings.length; i++){
        subShopping = subShoppings[i];

        subShopping.addEventListener("click",function(){
            proid = this.getAttribute("ga");
            $.post("/changecart/1/",{"productid":proid},function(data)
            {
                if(data.status === "success"){
                    //添加成功，吧中间的span的innetHTML变成当前的数量
                    document.getElementById(proid + "num").innerHTML=data.data.productnum;
                    document.getElementById(proid + "price").innerHTML = data.data.totalprice;
                    console.log("++++++++++++++++++++++++++++++++++++++++++");
                    if (data.data.productnum === 0)
                    {
                        var li = document.getElementById(proid + "li");
                        li.parentNode.removeChild(li)
                    }
                }
            })

        })
    }

    var  ischoses = document.getElementsByClassName("ischose");

    for(var j = 0; j < ischoses.length; j ++)
    {
        ischose = ischoses[j];

        ischose.addEventListener("click",function(){
            proid = this.getAttribute("goodsid");
            $.post("/changecart/2/",{"productid":proid},function(data)
            {
                if(data.status === "success") {

                    var s = document.getElementById(proid + "select");
                    s.innerHTML = data.data.str;

                }

            },false)

        })

    }


    var ok = document.getElementById("ok");
    ok.addEventListener("click",function(){
        var f = confirm("是否确认下单？");
        if (f)
        {
            // $.post("/saveorder/",function (data){
            $.post("/saveorder_d/",function (data){

                if(data.status === "success")
                {
                    window.location.href = "http://127.0.0.1:8000/order-to-pay/0/"
                    // window.location.href = "http://127.0.0.1:8000/cart/"; //新添加下单 详情列表环节
                }
                else if(data.status === "error"){

                    alert("请选择商品！");
                    window.location.href = "http://127.0.0.1:8000/cart/"; //新添加下单 详情列表环节
                }

                
            })

        }

    })

},false);


