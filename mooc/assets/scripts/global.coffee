# Utils for MOOC.

$ ->

    MOOC_Utils = {}

    MOOC_Utils.fade_out = (_element) ->
        _element.children('div').removeClass('bind-animate');
        _element.children('div').slideUp();
        _element.children('div').addClass('fade-out');
        setTimeout ->
            _element.remove();
            return;
        , 500;
        return ;

    MOOC_Utils.bindAction = ->
        $("#flash-messages-container > a").click ->
            $T.fade_out $(this)
            return;
        $(".message-box-fixed").children("a").children("div").each ->
            element_padding = $(this).css('padding').split(' ')[1].replace('px', '')
            element_width = $(this).width() + element_padding * 2;
            $(this).css({'margin-left': '-' + element_width / 2 + 'px'});

    MOOC_Utils.fadeOut = ->
        setTimeout ->
            $T.fade_out($("#flash-messages-container > a"));
            return;
        , 2500
        return ;

    MOOC_Utils.flash_message = (message, category) ->
        if typeof category == 'undefined' 
            category = 'notice'
        a_html = $('<a href="javascript:void(0)" class="message-box-btn close-btn"></a>').append($('<div class="flash-message-box bind-animate message-box-' + category + '"></div>').append(message))
        clear_html = $('<div style="clear:both;"></div>')
        $("#flash-messages-container").append(a_html)
        $("#flash-messages-container").append(clear_html)
        $T.bindAction()
        $T.fadeOut()
        return;


    MOOC_Utils.ajax_form = (form) ->
    # Json response API:
    # res.success: Whether operate successfully.
    # res.messages: Response messages.
        form.submit ->
            $('.message-tip-box').remove()
            $.ajax
                url: form.attr('action')
                dataType: 'json'
                data: form.serialize()
                type: form.attr('method')
                success: (res) ->
                    if (res.success)
                        if (res.messages)
                            $T.flash_message(res.messages.join(''), 'notice')
                        
                        if (res.jump_immediatelly)
                            timeout = 0;
                        else
                            timeout = 2000;
                        
                        if (res.next)
                            setTimeout ->
                                document.location = res.next
                            , timeout
                        else if (!res.stay)
                            setTimeout ->
                                document.location = document.referrer;
                            , timeout
                        
                        if (res.callback)
                            eval(res.callback + '(res, form.serializeObject())')
                    else
                        if (res.errors)
                            for key of res.messages
                                if (key == 'csrf_token')
                                    $T.flash_message(res.messages[key])
                                    continue
                                container = $('<div class="message-tip-box" id="message-' + key + '"></div>');
                                $('#' + key).before(container);
                                $('#' + key).on 'focus', ->
                                    $('#message-' + $(this).attr('id')).fadeOut()
                                container.append('<span>' + res.messages[key] + '</div>');
                        else
                            $T.flash_message(res.messages.join(''), 'warn')
                    return ;
                statusCode: {
                    404: ->
                        $T.flash_message('您请求的页面未找到', 'error')
                    405: ->
                        $T.flash_message('您未登录，无法进行操作', 'error')
                        return ;
                    },
                errors: (res) ->
                    $T.flash_message('Server Error', 'error')
                    return ;
            return false;
        return false;

    window.MOOC_Utils = window.$T = MOOC_Utils;

    $T.bindAction()
    $T.fadeOut()

    return;
