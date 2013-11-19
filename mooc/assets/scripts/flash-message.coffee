$ ->
    fade_out = (_element) ->
        _element.children('div').removeClass('bind-animate');
        _element.children('div').addClass('fade-out');
        setTimeout ->
            _element.remove();
            return;
        , 500;
        return ;

    $("#flash-messages-container > a").click ->
        fade_out $(this)
        return;

    setTimeout ->
        fade_out($("#flash-messages-container > a"));
        return;
    , 2500
    return;
