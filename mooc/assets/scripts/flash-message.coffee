$ ->
    $("#flash-messages-container > a").click ->
        _element = $(this);
        $(this).children('div').removeClass('bind-animate');
        $(this).children('div').addClass('fade-out');
        setTimeout ->
            _element.remove();
            return;
        , 200;
        return ;
    return;