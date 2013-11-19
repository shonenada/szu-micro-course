$ ->

    fade_out = (_element) ->
        _element.children('div').removeClass('bind-animate');
        _element.children('div').slideUp();
        _element.children('div').addClass('fade-out');
        setTimeout ->
            _element.remove();
            return;
        , 500;
        return ;

    $("#flash-messages-container > a").click ->
        fade_out $(this)
        return;

    $(".message-box-fixed").children("a").children("div").each ->
        element_padding = $(this).css('padding').split(' ')[1].replace('px', '')
        element_width = $(this).width() + element_padding * 2;
        $(this).css({'margin-left': '-' + element_width / 2 + 'px'});

    # setTimeout ->
    #     fade_out($("#flash-messages-container > a"));
    #     return;
    # , 2500

    return;
