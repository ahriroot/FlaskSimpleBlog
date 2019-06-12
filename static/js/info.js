function get(val) {
    $.post('/info/',{
        id: val,
    }, function(data) {
        $("#content").html(data);
    });
}
function on_click(val) {
    $.post('/info/',{
        id: val,
    }, function(data) {
        $("#content").html(data);
    });
    $.get('/comment/',{
        id: val,
    }, function(d) {
        $(".comment").html(d);
    });
}
function send(val) {
    $.post('/comment/',{
        id: val,
        content: editor.txt.html(),
    }, function(data) {
        if(data == 'ok'){
            $.get('/comment/',{
                id: val,
            }, function(d) {
                $(".comment").html(d);
            });
            alert('提交成功');
            editor.txt.html('')
        } else {
            window.location.href="/login";
        }
    });
}

let $1 = $(function () {
    $(".top").click(function () {
        $('html,body').animate({scrollTop: 0}, 300);
    });
    $(".bottom").click(function () {
        $('html,body').animate({scrollTop: 10000}, 500);
    });
});