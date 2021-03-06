
// submit product update form
$('#affiliate_application').submit(function(e){
  e.preventDefault();
  $.ajax({
    url:$(this).attr('action'),
    method:$(this).attr('method'),
    data:$(this).serialize(),
    success:function(){
      $('.received').html('');
      $('.received').text('Your request received. We will get back to you shortly.')
      $('#affiliate_application')[0].reset();
      setTimeout(function(){ 
        $('.affiliate-container').css({'display':'none'});
        $('.affiliate-design').css({'display':'inline-block',});
        $('.affiliate-container').removeClass('zoomIn');
        $('footer').show();
       $('header').show();
        
        ; }, 2000);
   
    },
    error:function(){}
  })
})


// when user clicks on submit form

$(document).ready(function(){
$('.register-form').click(function(){
  
$('.affiliate-container').css({'display':'inherit','position':'fixed'});
$('.affiliate-container').addClass('zoomIn');
$('.affiliate-design').css({'display':'none'});
$('footer').hide();
$('header').hide();
}); 
});


//check if a div is in viewport
$(document).ready(function(){
  $.fn.isInViewport = function() {
    var elementTop = $(this).offset().top;
    var elementBottom = elementTop + $(this).outerHeight();
  
    var viewportTop = $(window).scrollTop();
    var viewportBottom = viewportTop + $(window).height();
  
    return elementBottom > viewportTop && elementTop < viewportBottom;
  };
  /* 
  check if venture div is in view port perform the following actions
  */
  $(window).on('resize scroll', function() {
    $('.affiliate-info-container').each(function() {
        
      if ($(this).isInViewport()) {
          $('.aff-art-one').addClass('rotateIn ')

      } else {
        $('.aff-art-one').removeClass('rotateIn ')
      }
    });
  });

  /* wheck if main menu still on view port*/

  $(window).on('resize scroll', function() {
    $('#aa-header').each(function() {
        
      if ($(this).isInViewport()) {
        $('.fixed-menu').css({'height':'0px','padding-top':'0px','padding-bottom':'0px','visibility':'hidden'})

      } else {	
        $('.fixed-menu').css({'visibility':'initial','padding-top':'10px','padding-bottom':'10px','height':'auto','visibility':'initial'})
      }
    });
  });
})


// submit form when Qt change in cart 

function QuantityUpdate(form){
   var $this= $(this)
  $.ajax({
    url:$(form).attr('action'),
    method:$(form).attr('method'),
    data:$(form).serialize(),
    success:function(data){
      if (data){
        var salesprice =Math.round(data.objs.sale)+".00"
        var cost       = Math.round(data.objs.cost) + ".00"
       if(salesprice){
        $(".c-sales",form).text(salesprice+" " +'CFA')
       }
       if(cost){
        $(".c-cost",form).text(cost+" " +'CFA')}
      }
      $('.pd-count').text(data.objs.pdcount);
      $('.p-sum').text('CFA' +" "+data.objs.sum);
    },
    error:function(){
      
    }
  });
}


// add product to cart 
$(document).ready(function(){
 
$('#add-product-cart').submit(function(e){
 
e.preventDefault();

$('.loader_').show();

var method_ = $(this).attr('method');
var url_    = $(this).attr('action');
var data_   = $(this).serialize();
$.ajax({
  url:url_,
  method:method_,
  data:data_,
  success:function(data){
    $('#cart').text(data.cart);
    $('#cart-fixed').text(data.cart);
    $('.loader_').hide();
    $('.mainbody').css({'overflow':'initial','height':'initial'});
    $('.product-detail-container').hide();
    $('html, body').animate({ scrollTop: $('.product-detail-container').offset().top }, 'slow');
    $('#hidde_div').css({'display':'inherit'});
    $('#hidde_div_color').css({'display':'inherit'});
    $('.added_product').addClass('pulse');
    $('.product_dply').addClass('fadeInLeft');
    $('.product_detail').hide();
  },
  error:function(){
    setTimeout(function(){
      $('.loader_').hide();
      $('.instruction_').show(); 
      ; }, 3000);

  }
});
});
});


// when adding products to cart
$(document).ready(function(){
// when user selects a product size

$('.select-size').click(function(){
  var this_ = $(this);
  $('.price_display').hide();
  $('.selected_value').css({'border-color':'black','background-color':'white','color':'black'})
  if (!$('input',this).is(':checked')){
    console.log($('input',this).val())
   $('.selected_value',this).css({'border-color':'red','background-color':'red','color':'white'});
   $('input',this).prop('checked',true);
   $('.price_display',this).show();
   
   
  }
 
 
 });
});




// product post form 
// ajax form submit 
// reset form process



function processrest(){
  $('.section-two,.section-three').hide();
  $('.section-one').show();
 
  $('.alertsub').css({'display':'initial'});

    setTimeout(function(){ $('.alertsub').css({'display':'none'}); }, 6000);
}
 
// reset all preview
function previewreset() {
  $('#prev4').attr('src', '/static/img/df-pd-img/default.png');
  $('#prev1').attr('src', '/static/img/df-pd-img/default.png');
  $('#prev2').attr('src', '/static/img/df-pd-img/default.png');
  $('#prev3').attr('src', '/static/img/df-pd-img/default.png');
  $('.imgpreview .imgrm #rmfour').css({'visibility':'hidden'});
  $('.imgpreview .imgrm #rmone').css({'visibility':'hidden'});
  $('.imgpreview .imgrm #rmtwo').css({'visibility':'hidden'});
  $('.imgpreview .imgrm #rmthree').css({'visibility':'hidden'});

}

// reset input

    // reset input file
    resetinput();
    function resetinput(){
    $("#id_picone").val('');
    $("#id_pictwo").val('');
    $("#id_picthree").val('');
    $("#id_picfour").val('');
};

//update orderstate

$(document).ready(function(){
$('.orderstateupadate').submit(function(e){
  e.preventDefault();
  $('.databaseupdated',this).fadeIn('slow')
  $('.databaseupdated').delay(10000).fadeOut('slow')
  var this_   =$(this);
  var method_ =this_.attr('method');
  var action_ = this_.attr('action');
  var data_   = this_.serialize();
$.ajax({
  url:action_,
  method:method_,
  data:data_,
  success:function(data,this_){

  },
  error:function(data){

  }
})
});
});


/* whe shopper cancels an order */
$(document).ready(function(){
  $('#requestform').submit(function(e){
    e.preventDefault();
    $('h4').fadeIn('slow')
    $(' h4').delay(10000).fadeOut('slow')
    var this_   =$(this);
    var method_ =this_.attr('method');
    var action_ = this_.attr('action');
    var data_   = this_.serialize();
  $.ajax({
    url:action_,
    method:method_,
    data:data_,
    success:function(){
       $('#requestform')[0].reset()
    },
    error:function(data){
  
    }
  })
  });
  });

$(document).ready(function(){
  $('#ordercanceled').submit(function(e){
    e.preventDefault();
    $('.databaseupdated',this).fadeIn('slow')
    $('.databaseupdated').delay(10000).fadeOut('slow')
    $('button',this).attr('disabled',true)
    var this_   =$(this);
    var method_ =this_.attr('method');
    var action_ = this_.attr('action');
    var data_   = this_.serialize();
  $.ajax({
    url:action_,
    method:method_,
    data:data_,
    success:function(data,this_){
  
    },
    error:function(data){
  
    }
  })
  });
  });

$(document).ready(function(){
// submit contact form

$('#contactform').submit(function(e){
  e.preventDefault();
  $.ajax({
    url:$(this).attr('action'),
    method:$(this).attr('method'),
    data:$(this).serialize(),
    success:function(){
      $('.received').html('');
      $('.received').text('Message sent. Thank you')
      $('#contactform')[0].reset();
    },
    error:function(){}
  })
})



// submit product update form
$('#productupdateform').submit(function(e){
  e.preventDefault();
  $.ajax({
    url:$(this).attr('action'),
    method:$(this).attr('method'),
    data:$(this).serialize(),
    success:function(){
      $('#productupdateform p').text('This product updated')
    },
    error:function(){}
  })
})

//  submit product form
$('#productform').submit(function(e){
e.preventDefault();
$('#productform').ajaxSubmit({})
var  picone = $('#id_picone').val();
var pictwo  = $('#id_pictwo').val();
var picthree = $('#id_picthree').val();
var picfour  = $('#id_picfour').val();
if(picone !="" && pictwo!="" && picthree!="" && picfour!=""){

$('.gif img').show();
var this_   =$(this);
var method_ =this_.attr('method');
var action_ = this_.attr('action');
var data_   = this_.serialize();
$.ajax({

  success:function(){
    $('#productform')[0].reset();
    resetinput();
    previewreset();
    processrest();
    $('.gif img').hide();
    

  },
  error:function(){

  }
});
} 
});
});
$(document).ready(function(){

// when user clicks the next button 

$('.form-container .nextstep').click(function(){
    // do checks to make sure the values enter is not empty
    // inform first section
    var pdname = $('#id_productname');
    var pdct   = $('#id_category');
    var subct  = $('#id_subcategory');
    var size   = $('#id_size');
    var model  = $('#id_model');
    var color  = $('#id_color');
    var inputone   = pdname.val().replace(/^\s+|\s+$/g, "");
    var inputtwo   = pdct.val().replace(/^\s+|\s+$/g, "");
    var inputthree = subct.val().replace(/^\s+|\s+$/g, "");
    var inputfour   = color.val().replace(/^\s+|\s+$/g, "");
    var inputfive  = size.val().replace(/^\s+|\s+$/g, "");
    var inputsix   = model.val().replace(/^\s+|\s+$/g, "");


    if(inputone.length==0)

    {
       pdname.css({'border-bottom':'solid','border-color':'red','border-width':'1px'}); 
    }
    else{
        pdname.css({'border-bottom':'solid','border-width':'1px','border-color':'rgba(0,0,0,0.4)'}); 
    }

    if(inputfour.length==0)

    {
       color.css({'border-bottom':'solid','border-color':'red','border-width':'1px'}); 
    }
    else{
        color.css({'border-bottom':'solid','border-width':'1px','border-color':'rgba(0,0,0,0.4)'}); 
    }
    if( inputtwo.length==0){
        pdct.css({'border-bottom':'solid','border-color':'red','border-width':'1px'}); 
    }
    else {
        pdct.css({'border-bottom':'solid','border-width':'1px','border-color':'rgba(0,0,0,0.4)'});
    }
    if(inputthree.length==0){
        subct.css({'border-bottom':'solid','border-color':'red','border-width':'1px'}); 
    }
    else {
        subct.css({'border-bottom':'solid','border-width':'1px','border-color':'rgba(0,0,0,0.4)'});
    }

    if(inputfive.length == 0){
        size.css({'border-bottom':'solid','border-color':'red','border-width':'1px'}); 
    }
    else {
        size.css({'border-bottom':'solid','border-width':'1px','border-color':'rgba(0,0,0,0.4)'});
    }
    if(inputsix.length == 0){
        model.css({'border-bottom':'solid','border-color':'red','border-width':'1px'}); 
    }
    else {
        model.css({'border-bottom':'solid','border-width':'1px','border-color':'rgba(0,0,0,0.4)'});
    }


// if all field not empty , go to the next form section
    if(inputfour!=0 &&  inputtwo!=0 && inputthree!=0  && inputfive!=0 && inputsix !=0){
        $('.form-container .section-one').hide();
        $('.form-container .section-two').show();

        
    }
 
});

// when user clicks the nextsecond button
$('.form-container .nextsecond').click(function(){

    // define var
    var brand        = $('#id_brand');
    var location     = $('#id_location');
    var description  = $('#id_descript');
    var price  = $('#id_pdprice');
    var state  = $('#id_state');

    var input5      = price.val().replace(/^\s+|\s+$/g, "");
    var input1      = brand.val().replace(/^\s+|\s+$/g, "");
    var input2      = location.val().replace(/^\s+|\s+$/g, "");
    var input3      = description.val().replace(/^\s+|\s+$/g, "");
    var input4      = state.val().replace(/^\s+|\s+$/g, "");
    
    if( input5.length==0){
      price.css({'border-bottom':'solid','border-color':'red','border-width':'1px'}); 
  }
  else {
      price.css({'border-bottom':'solid','border-width':'1px','border-color':'rgba(0,0,0,0.4)'});
  }

  if( input4.length==0){
    state.css({'border-bottom':'solid','border-color':'red','border-width':'1px'}); 
}
else {
    state.css({'border-bottom':'solid','border-width':'1px','border-color':'rgba(0,0,0,0.4)'});
}

    if( input1.length==0){
        brand.css({'border-bottom':'solid','border-color':'red','border-width':'1px'}); 
    }
    else {
        brand.css({'border-bottom':'solid','border-width':'1px','border-color':'rgba(0,0,0,0.4)'});
    }
    if(input2.length==0){
        location.css({'border-bottom':'solid','border-color':'red','border-width':'1px'}); 
    }
    else {
        location.css({'border-bottom':'solid','border-width':'1px','border-color':'rgba(0,0,0,0.4)'});
    }
    if(input3.length==0){
        description.css({'border-bottom':'solid','border-color':'red','border-width':'1px'}); 
    }
    else {
        description.css({'border-bottom':'solid','border-width':'1px','border-color':'rgba(0,0,0,0.4)'});
    }
    
    // if all field not empty , go to the next form section
    if(  input5!=0 && input1!=0 && input2!=0 && input3!=0 && input4!=0){
        $('.form-container .section-one').hide();
        $('.form-container .section-two').hide();
        $('.form-container .section-three').show();
 
    }
});
});

// image preview  function
$(document).ready(function(){
// when user clicks to remove first image 

$('.imgpreview .imgrm #rmone').click(function(){
  // call image preview remove function for image one function
  rmprvone();
});

// image two removed
$('.imgpreview .imgrm #rmtwo').click(function(){
  // call image preview remove function for image one function
  rmprvtwo();
});

$('.imgpreview .imgrm #rmthree').click(function(){
  // call image preview remove function for image one function
  rmprvthree();
});

$('.imgpreview .imgrm #rmfour').click(function(){
  // call image preview remove function for image one function
  rmprvfour();
});

// remove image preview and set the initial image

function rmprvone() {
      $('#prev1').attr('src', '/static/img/df-pd-img/default.png');
      $('#id_picone').show();
      $('#id_picthree').hide();
      $('#id_picfour').hide();
      $('#id_pictwo').hide();
      $('.imgpreview .imgrm #rmone').css({'visibility':'hidden'});
     // set upload fild to empty
     $("#id_picone").val('');
  
}
// remove second uploaded image 

function rmprvtwo() {
  $('#prev2').attr('src', '/static/img/df-pd-img/default.png');
  $('#id_picone').hide();
  $('#id_picthree').hide();
  $('#id_picfour').hide();
  $('#id_pictwo').show();
  $('.imgpreview .imgrm #rmtwo').css({'visibility':'hidden'});
 // set upload fild to empty
 $("#id_pictwo").val('');

}


function rmprvthree() {
  $('#prev3').attr('src', '/static/img/df-pd-img/default.png');
  $('#id_picone').hide();
  $('#id_picthree').show();
  $('#id_picfour').hide();
  $('#id_pictwo').hide();
  $('.imgpreview .imgrm #rmthree').css({'visibility':'hidden'});
 // set upload fild to empty
 $("#id_picthree").val('');

}

function rmprvfour() {
  $('#prev4').attr('src', '/static/img/df-pd-img/default.png');
  $('#id_picone').hide();
  $('#id_picthree').hide();
  $('#id_picfour').show();
  $('#id_pictwo').hide();
  $('.imgpreview .imgrm #rmfour').css({'visibility':'hidden'});
 // set upload fild to empty
 $("#id_picfour").val('');

}


    // when  user upload the first pic

    function previewone(input) {
        if (input.files && input.files[0]) {
          var reader = new FileReader();
          
          reader.onload = function(e) {
            $('#prev1').attr('src', e.target.result);
            $('#id_picone').hide();
            $('#id_pictwo').show();
            $('.imgpreview .imgrm #rmone').css({'visibility':'initial'});
          }
          
          reader.readAsDataURL(input.files[0]);
        }
      }

      function previewtwo(input) {
        if (input.files && input.files[0]) {
          var reader = new FileReader();
          
          reader.onload = function(e) {
            // when user upload the second pic
            $('#prev2').attr('src', e.target.result);
            $('#id_picone').hide();
            $('#id_pictwo').hide();
            $('#id_picthree').show();
            $('.imgpreview .imgrm #rmtwo').css({'visibility':'initial'});
          }
          
          reader.readAsDataURL(input.files[0]);
        }
      }

      function previewthree(input) {
        if (input.files && input.files[0]) {
          var reader = new FileReader();
          
          reader.onload = function(e) {
            // when user upload the second pic
            $('#prev3').attr('src', e.target.result);
            $('#id_picone').hide();
            $('#id_pictwo').hide();
            $('#id_picthree').hide();
            $('#id_picfour').show();
            $('.imgpreview .imgrm #rmthree').css({'visibility':'initial'});
          }
          
          reader.readAsDataURL(input.files[0]);
        }
      }
      
      function previewfour(input) {
        if (input.files && input.files[0]) {
          var reader = new FileReader();
          
          reader.onload = function(e) {
            
            // when user upload the second pic
            $('#prev4').attr('src', e.target.result);
            $('#id_picone').show();
            $('#id_pictwo').hide();
            $('#id_picthree').hide();
            $('#id_picfour').hide();
            $('.imgpreview .imgrm #rmfour').css({'visibility':'initial'});
          }
          
          reader.readAsDataURL(input.files[0]);
        }
      }

      $("#id_picone").change(function() {
        previewone(this);
      });
      $("#id_pictwo").change(function() {
        previewtwo(this);
      });
      $("#id_picthree").change(function() {
        previewthree(this);
      });
      $("#id_picfour").change(function() {
        previewfour(this);
      });
});