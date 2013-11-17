$ ->
    $(".flash-message-box > a").click ->
        $(this).parent("div").fadeOut();
        return ;
