$(document).ready(function(){
    var account = document.getElementById("account");//定位到账户节点
    var passwd = document.getElementById("passwd");//密码设置
    var passwd2 = document.getElementById("passwd2");//密码验证


    var accounterr = document.getElementById("accounterr");//定位到账户输入不正确的节点
    var checkerr = document.getElementById("checkerr");//账户是否已经存在节点
    var passwderr = document.getElementById("passwderr");//密码格式错误节点
    var passwd2err = document.getElementById("passwd2err");//两次密码不同节点

    accounterr.style.display = "none";
    checkerr.style.display = "none";
    passwderr.style.display = "none";
    passwd2err.style.display = "none";


    account.addEventListener("focus",function(){
        accounterr.style.display = "none";
        checkerr.style.display = "none";
    },false);
    account.addEventListener("blur",function(){
        var inputStr = this.value;
        if(inputStr.length < 6 || inputStr.length > 12){
            accounterr.style.display = "block";
            // return
        }

        $.post("/checkuserid/",{"userid":inputStr}, function(data){

            if(data.status === 'error'){
                checkerr.style.display = "block"
            }
        })
    },false);

    passwd.addEventListener("focus",function(){
        passwderr.style.display = "none";
    },false);
    passwd.addEventListener("blur",function(){
        var inputStr = this.value;
        if(inputStr.length < 6 || inputStr.length > 12){
            passwderr.style.display = "block";
            // return
        }
    },false);
    passwd2.addEventListener("focus",function(){
        passwd2err.style.display = "none";
    },false);
    passwd2.addEventListener("blur",function(){
        var inputStr = this.value;
        if(inputStr !== passwd.value){
            passwd2err.style.display = "block";
            // return
        }
    },false);



    // passwd2.addEventListener("focus",function(){
    //     // accounterr.style.display = "none";
    //     // checkerr.style.display = "none";
    // },false);










})