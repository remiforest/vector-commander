$(document).on('keydown',function(e){
    console.log(e.key);
    $.ajax({
        url: "keydown",
        type: 'post',
        data: {"key":e.key},
        success:function(data){
            console.log(data)
        }
    });
})

$(document).on('keyup',function(e){
    $.ajax({
        url: "keyup",
        type: 'post',
        data: {"key":e.key},
        success:function(data){
            console.log(data)
        }
    });
})
