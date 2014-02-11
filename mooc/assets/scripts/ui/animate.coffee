$ ->
    $(".course-container").mouseover(->
        $(this).removeClass("container-animate-move-down");
        $(this).addClass("container-animate-move-up");
    );
    $(".info-wraper").mouseover(->
        $(this).removeClass("container-animate-move-down");
        $(this).addClass("container-animate-move-up");
    );
    $(".course-container").mouseleave(->
        $(this).removeClass("container-animate-move-up");
        $(this).addClass("container-animate-move-down");
    );
    $(".info-wraper").mouseleave(->
        $(this).removeClass("container-animate-move-up");
        $(this).addClass("container-animate-move-down");
    );
