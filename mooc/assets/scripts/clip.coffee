$ ->
    $(".clip-btns").click ->
        _name = $(this).attr("id").replace("btn", "clip")
        $(".clip-bar").addClass("clip-hidden")
        $("#" + _name).removeClass("clip-hidden")
        $(".clip-btns").removeClass("current")
        $(this).addClass("current")
        return ;