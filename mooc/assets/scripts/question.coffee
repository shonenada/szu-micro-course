$ ->

    vote = (aid, action) ->
        $.ajax {
            url: '/discuss/question/vote'
            dataType: 'json'
            data: {'aid': aid, 'action': action}
            type: 'POST'
            success: (res) ->
                if (res.success)
                    $T.flash_message(res.message)
                    count = parseInt $("#answer-" + aid + " .up_count a").html()
                    if (action == 'up')
                        $("#answer-" + aid + " .up_count a").html(count + 1)
                        $("#answer-" + aid + " .vote-up").addClass("vote-btn-click")
                    else if (action == 'down')
                        $("#answer-" + aid + " .up_count a").html(count - 1)
                        $("#answer-" + aid + " .vote-down").addClass("vote-btn-click")
                    return ;
                else
                    $T.flash_message(res.message, 'error')
                    return ;
                return ;
            statusCode: {
                405: ->
                    $T.flash_message('您未登录，无法进行操作', 'error')
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
            url: $(this).attr('action')
            dataType: 'json'
            data: $(this).serialize()
            type: 'POST'
            success: (res) ->
                if (res.success)
                    $T.flash_message('提交成功')
                    setTimeout ->
                        document.location = document.location;
                        return ;
                    , 1000
                    return ;
                else
                    $T.flash_message(res.message, 'error')
                    return ;
                return ;
            statusCode: {
                405: ->
                    $T.flash_message('您未登录，无法进行操作', 'error')
                    return ;
                }
            }
        return false;
