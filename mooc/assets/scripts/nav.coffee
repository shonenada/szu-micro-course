$ ->
    thisUrl = document.location.toString().toLowerCase();
    group = $('#nav li').children('a');
    for g in group
        if thisUrl == g.toString()
            $(g).addClass('nav_current');
    return ;

$ ->
    $(".dropdown-nav .dropdown").hide();
    $('.dropdown-nav').miniDropdown {animation: 'slide', show: 100, hide: 100, delayIn: 100, delayOut: 100}
