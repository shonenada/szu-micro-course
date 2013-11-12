$ ->
    thisUrl = document.location.toString().toLowerCase();
    group = $('#nav li').children('a');
    for g in group
        if thisUrl == g.toString()
            $(g).addClass('nav_current');
    return ;
