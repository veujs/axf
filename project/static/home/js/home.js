$(document).ready(function(){
    // setTimeout() 方法用于在指定的毫秒数后调用函数或计算表达式---setTimeout(code,millisec)
    setTimeout(function () {
        swiper1();
        swiper2();
    },100)
});


function swiper1(){
    var mySwiper1 = new Swiper("#topSwiper", {
        direction: 'horizontal',
        loop: true,
        speed: 500,
        autoplay: 2000,
        pagination:".swiper-pagination",
        control: true
    })
}
function swiper2(){
    var mySwiper2 = new Swiper("#swiperMenu", {
        slidesPerView: 3,
        loop: false,
        pagination : '.swiper-pagination',
        paginationClickable: true,//此参数设置为true时，点击分页器的指示点分页器会控制Swiper切换。
        spaceBetween:2
    })
}


