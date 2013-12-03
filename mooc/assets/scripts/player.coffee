$ ->
    data = new Array()
    checkTimer = null

    get_json_data = (lid) ->
        $.ajax {
                url: '/lecture/' + lid + '/questions',
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
            if (Math.abs(currentTime - item.time) < 0.5)
                $("#player-mask > form > .opts").empty()
                $("#player-mask").height($("#player-container").height() - 120)
                $("#player-mask").width($("#player-container").width() - 200)
                $("#player-mask > form >.quetion").html(item.q)
                for op in item.a
                    $("#player-mask > form > .opts").append("<label><input name='answer' type='radio' value=''>" + op + "</input></label>")
                $("#player-mask").show()
                clearInterval(checkTimer)
                obj.pause()
        return ;

    $("#continue-btn").click ->
        obj = document.getElementById('player')
        $("#player-mask").hide()
        checkTimer = setInterval(check_duration, 1000)
        obj.play()

    $("#skip-btn").click ->
        obj = document.getElementById('player')
        $("#player-mask").hide()
        checkTimer = setInterval(check_duration, 1000)
        obj.play()

    $("#player-mask").hide()
    get_json_data(1)
    checkTimer = setInterval(check_duration, 1000)
    return ;
