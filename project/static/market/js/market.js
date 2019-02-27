$(document).ready(function(){





    var alltypebtn = document.getElementById("alltypebtn");
    var showsortbtn = document.getElementById("showsortbtn");

    var typediv = document.getElementById("typediv");
    var sortdiv = document.getElementById("sortdiv");

    typediv.style.display = "none";
    sortdiv.style.display = "none";

    alltypebtn.addEventListener("click",function(){
        typediv.style.display = "block";
        sortdiv.style.display = "none";
    },false);
    showsortbtn.addEventListener("click",function(){
        typediv.style.display = "none";
        sortdiv.style.display = "block";
    },false);
    typediv.addEventListener("click",function(){
        typediv.style.display = "none";
    },false);
    sortdiv.addEventListener("click",function(){
        sortdiv.style.display = "none";
    },false);


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

                    document.getElementById(proid).innerHTML=data.data["productnum"];
                    console.log("++++++++++++++++++++++++++++++++++++++++++");


                }else{
                    if(data.data === "do not login"){
                        console.log("************************************************");
                        window.location.href = "http://127.0.0.1:8000/login/"
                    }

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
                    document.getElementById(proid).innerHTML=data.data.productnum;
                    console.log("++++++++++++++++++++++++++++++++++++++++++");
                }else{
                    if(data.data === "do not login"){
                        console.log("************************************************");
                        window.location.href = "http://127.0.0.1:8000/login/"
                    }
                }
            })

        })
    }


    // var yellowSlides = document.getElementsByClassName("yellowSlide");
    //
    // for(i = 0; i < yellowSlides.length; i ++){
    //     // yellowSlide = yellowSlides[i];
    //     yellowSlides[i].parentElement.onclick = (function(){
    //         return function(){
    //             yellowSlide = yellowSlides[i];
    //             yellowSlide.style.background = 'red';
    //         }
    //     })(i);
    // }


});




