$ ->
    $(".lecture-btns").click ->
        _name = $(this).attr("id").replace("btn", "lecture")
        $(".lecture-bar").addClass("lecture-hidden")
        $("#" + _name).removeClass("lecture-hidden")
        $(".lecture-btns").removeClass("current")
        $(this).addClass("current")
        return ;