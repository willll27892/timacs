


$(document).ready(function(){
 
 var winwindth=$(window).width()
    // menu button click handling first and second clicked
    
    $('.mobile-menu svg').click(function() {

       // check if window width is greater than 990 
    if (winwindth>900){

    
  
    var clicks = $(this).data('clicks');
    if (clicks) {
        $('.nav-menu').css({'visibility':'hidden'});
        $('nav .info_name').css({'visibility':'hidden'});
        $('nav').css({'width':'0%'});
        $('.maincontainer').css({'width':'100%','left':'0%'});
    } else {
        $('.nav-menu').css({'visibility':'initial'});
        $('nav .info_name').css({'visibility':'initial'});
        $('.maincontainer').css({'width':'90%','left':'10%','transition':'width 1s','transition':'left 0s'});
        $('nav').css({'width':'15%','visibility':'initial'});
    }
    $(this).data("clicks", !clicks);
}


if (winwindth>150 && winwindth <400){

    var clicks = $(this).data('clicks');
    if (clicks) {
        $('nav').css({'width':'0%'});
              $('.maincontainer').css({'width':'100%','left':'0%'});
    } else {
       
        $('.maincontainer').css({'width':'100%','left':'60%','transition':'width 1s','transition':'left 0s'});
        $('nav').css({'width':'180px','visibility':'initial'});
    }
    $(this).data("clicks", !clicks);
}
 

  if (winwindth>400 && winwindth <600){

    var clicks = $(this).data('clicks');
    if (clicks) {
        $('nav').css({'width':'0%'});
              $('.maincontainer').css({'width':'100%','left':'0%'});
    } else {
       
        $('.maincontainer').css({'width':'100%','left':'30%','transition':'width 2s','transition':'left 0s'});
        $('nav').css({'width':'30%','visibility':'initial'});
    }
    $(this).data("clicks", !clicks);
}
  
if (winwindth>600 && winwindth <900){

    var clicks = $(this).data('clicks');
    if (clicks) {
        $('nav').css({'width':'0%'});
              $('.maincontainer').css({'width':'100%','left':'0%'});
    } else {
       
        $('.maincontainer').css({'width':'100%','left':'20%','transition':'width 2s','transition':'left 0s'});
        $('nav').css({'width':'20%','visibility':'initial'});
    }
    $(this).data("clicks", !clicks);
}
  
});
});

