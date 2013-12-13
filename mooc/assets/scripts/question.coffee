$ ->

    vote = (aid, action) ->
        $.ajax {
            url: '/question/vote'
            dataType: 'json'
            data: {'aid': aid, 'action': action}
            type: 'POST'
            success: (res) ->
                if (res.success)
                    window.flash_message(res.message)
                    count = parseInt $("#answer-" + aid + " .up_count a").html()
                    $("#answer-" + aid + " .up_count a").html(count + 1)
                    return ;
                else
                    window.flash_message(res.message, 'error')
                    return ;
                return ;
            statusCode: {
                405: ->
                    window.flash_message('您未登录，无法进行操作', 'error')
                    return ;
                }
            }
        return ;

    $(".vote-up").click ->
        aid = $(this).attr('data')
        vote(aid, 'up')
        return ;

    $(".vote-down").click ->
        aid = $(this).attr('data')
        vote(aid, 'down')
        return ;

    $("#re-answer-form").submit ->
        $.ajax {
            url: $("#re-answer-form").attr('action')
            dataType: 'json'
            data: $("#re-answer-form").serialize()
            type: 'POST'
            success: (res) ->
                if (res.success)
                    window.flash_message('提交成功')
                    setTimeout ->
                        location.reload()
                    , 2000
                    return ;
                else
                    window.flash_message(res.message, 'error')
                    return ;
                return ;
            statusCode: {
                405: ->
                    window.flash_message('您未登录，无法进行操作', 'error')
                    return ;
                }
            }
        return false;

    return ;
