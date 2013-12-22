$ ->
    
    data = new Array()
    checkTimer = null
    window.lecture_id = 0

    $(".player-mask").hide()

    window.register_lecture_id = (lecture_id) ->
        window.lecture_id = lecture_id
        get_json_data()
        checkTimer = setInterval(check_duration, 1000)
        return ;

    get_json_data = () ->
        $.ajax {
                url: '/lecture/' + window.lecture_id + '/questions',
                dataType: 'json',
                success: (items) ->
                    data = items
                    return;
            }
        return ;

    check_duration = () ->
        obj = document.getElementById('player')
        currentTime = obj.currentTime
        for item in data
            if (Math.abs(currentTime - item.time_at) < 0.5)
                $("#question-answer-mask > form > .opts").empty()
                $("#question-answer-mask > #question-form > .question > .tips").empty()
                $("#question-answer-mask").height($("#player-container").height() - 120)
                $("#question-answer-mask").width($("#player-container").width() - 200)
                $("#quiz_id").attr('value', item.id)
                $("#question-answer-mask > form > .question > .question-title").html(item.question)
                for op in item.options
                    $("#question-answer-mask > form > .opts").append("<label><input name='answer_id' type='radio' value='" + op.id + "'>" + op.content + "</input></label>")
                $("#question-answer-mask").show()
                clearInterval(checkTimer)
                obj.pause()
        return ;

    $("#continue-btn").click ->
        obj = document.getElementById('player')
        $.ajax {
                url: '/lecture/' + window.lecture_id + '/check',
                dataType: 'json',
                data: $('#question-form').serialize(),
                type: 'POST',
                success: (res) ->
                    if (res.success)
                        $("#question-answer-mask").hide()
                        $("#question-answer-mask > #question-form > .question > .tips").empty()
                        checkTimer = setInterval(check_duration, 1000)
                        obj.play()
                        return ;
                    else
                        $("#question-answer-mask > #question-form > .question > .tips").html "回答错误，请重新回答"
                        return ;
                    return ;
            }
        return ;


    $("#skip-btn").click ->
        obj = document.getElementById('player')
        $("#question-answer-mask").hide()
        checkTimer = setInterval(check_duration, 1000)
        obj.play()
        return ;

    return ;
