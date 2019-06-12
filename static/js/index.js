$(function () {
    let h = $(".art-name").height();
    if(h < 170){
        $("#more").hide();
    } else {
        $(".art-name").animate({height:'160px'},900);
    }
    $("#more").click(function () {
        if($(".art-name").height() == h){
            $("#more").rotate(0);
            $(".art-name").animate({height:"160px"},500);
        } else {
            $("#more").rotate(180);
            $(".art-name").animate({height:h+"px"},500);
        }
    });

    $(".art-name").mouseenter(function () {
        $(".art").css("color", "#333");
    });
    $(".art-name").mouseleave(function () {
        $(".art").css("color", "#888");
    });
    $(".art").mouseenter(function () {
        $(this).css("color", "#000");
    });
    $(".art").mouseleave(function () {
        $(this).css("color", "#333");
    });
});

$(function(){
    let goUp = $('.up');
    goUp.hide();
    $(window).scroll(function(){
        if($(this).scrollTop() > 10){
            $('.up').fadeIn();
        }else{
            $('.up').fadeOut();
        }
    });
    goUp.click(function(){
        $('html ,body').animate({scrollTop: 0}, 300);
        return false;
    });

    $('.send').click(function () {
        $('#feedback').slideToggle(400);
        // $('#feedback').toggle(100);
    });
});

function CheckInfo() {
    if (event.keyCode == 13) {
        $("#form").submit();
    }
}
function toInfo(val) {
    window.location.href = "/info?id="+val;
}
function toCate(val) {
    $.post('/art_by_cate/',{
        id: val,
    }, function(data) {
        $("#art_by_cate").html(data);
    });
}