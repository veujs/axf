$(document).ready(function(){

    var is_selects = document.getElementsByClassName("is_select");

    for(var i = 0; i < is_selects.length; i++){

        is_select = is_selects[i];
        console.log(is_select);
        is_select.addEventListener("click",function(data){
            console.log("000000000000000000000000000000000000000000");
            order_id = this.getAttribute("order_id");
            $.post('/change-order-select/',{"order_id":order_id},function(data){

                if(data.status === "success"){

                    var s = document.getElementById(order_id + "select");
                    s.innerHTML = data.data.str;
                }
            })
        })
    }





   var alipay = document.getElementById('alipay');
   alipay.addEventListener('click',function(data){
       var f = confirm("确认下单？");
       if(f)
       {
           $.post('/change-order-status/1/',function(data){
               if(data.status === 'success')
               {
                   window.location.href = "/order-to-pay/1/"

               }
           })

       }


   })



});