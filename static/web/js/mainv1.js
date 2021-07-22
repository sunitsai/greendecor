//
//$(window)click(function(event) {
//    $(".navbar-collapse").collapse('hide');
//
//    event.stopPropagation();
//});

// $(document).not("li.dropdown").click(function (event) {


$( "#ChangeToggle" ).click(function() {   // to stop scrolling when mobile menu is open
  $("body").css("overflow","hidden");
     var _opened = $("div#navbar").hasClass("in");
     if (_opened === true ) {
            $("body").css("overflow","auto");  // to re-enable scrolling when mobile menu is open

        }

});


 $(document).not("li.dropdown").click(function (event) {
//        console.log("first");
        var clickover = $(event.target);
        var _opened = $("div#navbar").hasClass("in");
//        console.log(_opened);
        if (_opened === true && !clickover.hasClass("navbar-toggle")) {
//            console.log("third");
            $("button.navbar-toggle").click();
//            $(".navbar-collapse").collapse('hide');

            $("body").css("overflow","auto");  // to re-enable scrolling when mobile menu is open



        }
    });



$('li.dropdown').click(function(){
	$('this').addClass('open').find('ul.dropdown-menu').animate({top:35},200)

})
$(function(){
    $('div.main-content').css('padding-top', $('header>nav.navbar').outerHeight()+$('div.mini-header').height()-10);
})
$(function() {
  $('a[href="#main"]').click(function() {
    if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'') && location.hostname == this.hostname) {
      var target = $(this.hash);
      target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
      if (target.length) {
        $('html,body').animate({
          scrollTop: target.offset().top
        }, 1000);
        return false;
      }
    }
  });
$('i.fa.fa-heart-o').click(function(){
    if($(this).hasClass('fa-heart-o')==true){
    $(this).removeClass('fa-heart-o').addClass('fa-heart').css({'color':'#dc9a19','border-color':'#dc9a19'});
    }else{
        $(this).removeClass('fa-heart').addClass('fa-heart-o').css({'color':'#999','border-color':'#999'});
    }
})
//hover menu
$('ul.menu-1').find('li').each(function(){
	$(this).hover(function() {
  $(this).stop( true, true ).addClass('open')
}, function() {
  $(this).stop( true, true ).removeClass('open')
});
})
//scrolling animation
	$(window).scroll(function(){
        if($(window).scrollTop()>200){
			$('nav.navbar.navbar-fixed-top').css({'-webkit-transition':'.25s ease-in','-moz-transition':'.25s ease-in','background-color': '#f9f9f9','top':'0px'});
			$('header nav ul.menu-1 li.dropdown').css({'padding':'20px 0px'});
			$('a.navbar-brand > img').css({'height':'56px','marginTop':'-10px','-webkit-transition':'.25s ease-in','-moz-transition':'.25s ease-in'});
			$('header nav ul.menu-1 li > a').css({'color':'#222','-webkit-transition':'.15s ','-moz-transition':'.15s ',});
            if(window.outerWidth<500){
                 $('header nav ul.menu-1 li > ul.dropdown-menu').css({'-webkit-transition':'.15s ','-moz-transition':'.15s ','background-color': '#f9f9f9','top': '81%'});
                $('nav.navbar.navbar-fixed-top').css({'padding':'10px 0px 2px','-webkit-transition':'.25s ease-in','-moz-transition':'.25s ease-in','background-color': '#f9f9f9','top':'0px'});
            }else{
            $('header nav ul.menu-1 li > ul.dropdown-menu').css({'-webkit-transition':'.15s ','-moz-transition':'.15s ','background-color': '#f9f9f9','top': '100%'});
            }
            $('div.mini-header').css({'top':'-37px','-webkit-transition':'.3s ease-in','-moz-transition':'.3s ease-in'});
            $('div.top-scrolling-btn-in-bottom').css('display','block');
		}else{
            if(window.outerWidth<500){
			$('nav.navbar.navbar-fixed-top').css({'-webkit-transition':'.25s ease-in','-moz-transition':'.25s ease-in','background-color': '#fff','top':'37px'});
				$('header nav ul.menu-1 li.dropdown').css({'padding':'35px 0px'});
            $('header nav ul.menu-1 li > ul.dropdown-menu').css({'-webkit-transition':'.15s ','-moz-transition':'.15s ','background-color': '#fff','top': '100%'});
            }else{
                $('nav.navbar.navbar-fixed-top').css({'-webkit-transition':'.25s ease-in','-moz-transition':'.25s ease-in','background-color': '#fff','top':'37px'});
				$('header nav ul.menu-1 li.dropdown').css({'padding':'35px 0px'});
            $('header nav ul.menu-1 li > ul.dropdown-menu').css({'-webkit-transition':'.15s ','-moz-transition':'.15s ','background-color': '#fff','top': '100%'});
            }
            $('header nav ul.menu-1 li > a').css({'color':'rgba(34, 34, 34, 0.87)','-webkit-transition':'.15s','-moz-transition':'.15s',});
			$('a.navbar-brand > img').css({'height':'100px','marginTop':'-17px','-webkit-transition':'.25s ease-in','-moz-transition':'.25s ease-in'});
            $('div.mini-header').css({'top':'0px','-webkit-transition':'.25s ease-in','-moz-transition':'.25s ease-in'})
            $('div.top-scrolling-btn-in-bottom').css('display','none');
        }
	});
});
//search poup
$('.dropdown a > i.fa.fa-search').click(function(){
    openSearch();
});
function closeSearch(){
    $('#search-modal').animate({'x':-2000}, {
            step: function(now,fx) {
                $(this).css('transform','translate3d(0px,'+now+'px,0px)');
            },duration:'3000'},'2000').removeClass('active');
            $('.search-box input.input').val()=='';
}
function openSearch(){

    $('#search-modal').animate({'x':0}, {
            step: function(now,fx) {
                $(this).css('transform','translate3d(0px,'+now+'px,0px)');
            },duration:'0'},'200').addClass('active').find('input#search-boxs').focus();
    $('input.button.btn-search').css('opacity','0.6')
    }
//search  buttonanimation
$('.search-box input.input').on({
    keydown:function(){
    $('form span').css({'font-size': '17px','color': '#dc9916','transition':'.3s ease-in'});
    $('input.button.btn-search').css('opacity','1');
    if(event.keyCode==8){
            if($(this).val()==''){
            $('form span').css({'font-size': '34px','color': '#999','transition':'.3s ease-in'});
            $('input.button.btn-search').css('opacity','5')
        }
        }
    },
    blur:function(){
        if($(this).val()==null){
            $('form span').css({'font-size': '34px','color': '#999','transition':'.3s ease-in'});
            $('input.button.btn-search').css('opacity','5')
        }
    }
})
$('.close-modal.col-md-12').click(function(){
    closeSearch();
})

/* tabs function */
$('ul.tabs > li').click(function(){
    $('div.tab-content').find('div.active-content').removeClass('active-content');
    $('ul.tabs > li').removeClass('active-tab');
    $(this).parents('div.tabs-sec').find('div.tab-content').find('div.'+this.className).addClass('active-content');
    $(this).addClass('active-tab');
    var he=$('.t.active-content').outerHeight(true);
    $(this).parents('div.tabs-sec').find('div.tab-content').css({'height':he+15+'px','max-height':he+35+'px'});
})
/* tabs function */
/*accordian function*/
$('.panel > .panel-title').click(function(){
    if($(this).parents('.panel').find('.panel-content').hasClass('in')==true){
        $(this).parents('.panel').find('.panel-content').slideUp(150).removeClass('in');
        $(this).find('i.fa').removeClass('fa-angle-up').addClass('fa-angle-down');
    }else if($('.panel-content').hasClass('in')==true && $(this).parents().is('.filter-sec')!=true){
        $('.panel-content').removeClass('in').slideUp(150);
        $('.panel-title').find('i.fa').removeClass('fa-angle-up').addClass('fa-angle-down');
        $(this).parents('.panel').find('.panel-content').slideDown(150).addClass('in');
        $(this).find('i.fa').removeClass('fa-angle-down').addClass('fa-angle-up');
    }else{
    $(this).parents('.panel').find('.panel-content').slideDown(150).addClass('in');
    $(this).find('i.fa').removeClass('fa-angle-down').addClass('fa-angle-up')
    }
});
$(function(){
   if( $('.panel > .panel-content').hasClass('in')){
       $('.panel > .panel-content.in').css('display','block')
   }
})
/* scrollin effect */
var w=$(window);
w.scroll(function(){
		if(w.scrollTop()>400&&w.scrollTop()<$('.col-md-9.faq-content').height()-100){
				$('.contact-form.single-service.col-md-4').css('top',w.scrollTop()-389+'px');
		}
});
//$('input.checkbox,.fullpage-search .filter-sec .category label').hover(function(){
//        $(this).attr('checked', true);
//},function(){
//    $(this).attr('checked', false);
//});
//toastr js start
$.fn.extend({
    toastr_alert:function(a){
        $('#toastr').animate({opacity:1,'right':'2%'},250).addClass('alert').find('span.toastr-content').html(a);
        setTimeout(function(){$('#toastr').animate({opacity:0,'right':'-30%'},250).removeClass('alert')},4000);
    },
    toastr_success:function(a){
        $('#toastr').animate({opacity:1,'right':'2%'},250).addClass('success').find('span.toastr-content').html(a);
        setTimeout(function(){$('#toastr').animate({opacity:0,'right':'-30%'},250).removeClass('success')},4000);
    },
    toastr_warning:function(a){
        $('#toastr').animate({opacity:1,'right':'2%'},250).addClass('warning').find('span.toastr-content').html(a);
        setTimout(function(){$('#toastr').animate({opacity:0,'right':'-30%'},250).removeClass('warning')},4000);
    }
});

//validation js
function validation_form_input(a){
    var t=$(a).attr('type');
        if(t=='text'||t=='tel'||t=='number'){
            if($(a).val()==''){
                $(a).addClass('shake').parent('div').css('position','relative').append('<span class="error-msg">This field is manadatory<i class="fa fa-star"></i></span>');
            }
        }else if(t=='email'){
            var r=/^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;;
             if($(a).val()==''){
                  $(a).addClass('shake');
             }else if(r.test($(this).val())==false){
                $(a).addClass('shake');
            }
        }
}
$.fn.extend({
submitform:function(){
    $(this).parents('form').find('input.validation').each(function(){
                    if($(this).val()==''){
                       $(this).addClass('shake').parent('div').css('position','relative').append('<span class="error-msg">This field is manadatory</span>');
                        event.preventDefault();
                    }
                });
},
input:function(){
$(this).on({
    focusout:function(){
        validation_form_input(this)
    },
    keyup:function(){
        if(event.keyCode==9||event.keyCode==13){
            if($(this).val()==''){
            validation_form_input(this);
            }
        }else  if($(this).val()!=''){
          $(this).removeClass('shake').parents('form').find('input.validation').removeAttr('disabled');
             $(this).parent('div').removeAttr('style').find('span').remove();
         }
    }
});
}
});
$('.validation').input();
$('.form-submit').click(function(){
    $(this).submitform();
});
$(function(){
    $('.share-change a.title').click(function(){
        if($(this).next('.social-share').hasClass('active-share')){
            $(this).next('.social-share').removeClass('active-share').animate({height:'0px','z-index':'-9'},400)

        }else{
            $(this).next('.social-share').addClass('active-share').animate({height:'180px','z-index':'9'},400)
        }
    });
});
$(function(){
     $('#review-scroll .review-testomanial div.write-review-box').slideUp(170);
    $('#review-scroll .review-testomanial .col-xs-12.text-center > a.button').click(function(){
    if($(this).parents('div.review-testomanial').find('div.write-review-box').hasClass('in')){
        $(this).parents('div.review-testomanial').find('div.write-review-box').slideUp(170).removeClass('in');
    }else{
    $(this).parents('div.review-testomanial').find('div.write-review-box').slideDown(170).addClass('in');
    }
});
    $('.show-pwd > i.fa.fa-eye').click(function(){
        if($(this).parent('div.show-pwd').find('input').attr('type')=='Password'){
            $(this).parent('div.show-pwd').find('input').attr('type','text')
        }else{
            $(this).parent('div.show-pwd').find('input').attr('type','Password');
        }
    });
});
//add search on popup
var search = instantsearch({
        appId: 'AGHBVMU77S',
        apiKey: 'b5fb475940558ecf9d3ea95a20603b6e',
        indexName: 'my_index',
		urlSync: true
      });

      search.addWidget(
        instantsearch.widgets.searchBox({
          container: '#search-boxs',
          placeholder: 'Search for products...'
        })
      );
var filterTemplate=' <div class="hollow-button">'+
                                '<a class="button {{#isRefined}}activetag{{/isRefined}}">{{name}}</a>'
                            +'</div>';
var header_temp='<div class="content-box col-xs-12 no-gutter"><h3 class="title-head font-size-16">Placement<span> tags</span></h3></div>';
var filterTemplate2=' <div class="col-xs-3 underline-button">'+
                                '<a class="button {{#isRefined}}activetag{{/isRefined}}">{{name}}</a>'
                            +'</div>';
var filterTemplate3=' <div class="col-xs-4 underline-button">'+
                                '<a class="button {{#isRefined}}activetag{{/isRefined}}">{{name}}</a>'
                            +'</div>';
search.addWidget(
          instantsearch.widgets.refinementList({
            container: '#placements',
            attributeName: '_tags',
            operator: 'or',
            sortBy: ['name:asc'],
            limit: 20,
            templates: {
			  header:header_temp,
              item: filterTemplate
            }
          })
        );
search.addWidget(
          instantsearch.widgets.refinementList({
            container: '#maintenance',
            attributeName: 'maintenance_level',
            operator: 'or',
            sortBy: ['name:asc'],
            limit: 10,
            templates: {
              item: filterTemplate
            }
          })
        );
search.addWidget(
          instantsearch.widgets.refinementList({
            container: '#seaso',
            attributeName: '_season',
            operator: 'or',
            sortBy: ['name:asc'],
            limit: 6,
            templates: {
              item: filterTemplate
            }
          })
        );
		search.addWidget(
          instantsearch.widgets.refinementList({
            container: '#fragranc',
            attributeName: 'fragrance',
            operator: 'or',
            sortBy: ['name:asc'],
            limit: 4,
            templates: {
              item: filterTemplate2
            }
          })
        );
search.start();
function redirectSearch(){
	if(window.location.search==''&&$('#search-boxs').val()!=""){
		window.location.href='//'+window.location.host+'/search/?q='+$('#search-boxs').val();
	}else{
	window.location.href='//'+window.location.host+'/search/'+window.location.search;
	}
}
function forDelayinExcute(){

}
$(document).on({
	keypress:function(){
		if(event.currentTarget.id=='search-boxs'||event.currentTarget.activeElement.id=='search-boxs'){
			if(event.keyCode==13||event.keyCode==9){
			event.preventDefault();
			redirectSearch();
		}
		}
    },
	click:function(){
			   	if($(event.target).parents('div').is('#search-modal')&&($(event.target).parents('div').is('.content-hollow')||$(event.target).parents('div').is('.content-type'))){
					$(event.target).parents('div#search-modal').append('<div class="transparent"></div>');
					var elem=event.target.parentElement;
						setInterval(function(){
							if($('a.button').is('.activetag')&&$('a.button').parents('div').is('#search-modal')&&($('a.button').parents('div').is('.content-hollow')||$('a.button').parents('div').is('.content-type'))){
								redirectSearch();
							}
						}, 3000);
				}
	}
});


if($(window).width()< 991){

		$("#close").click(function() {
					$("#close").css("display", "none");
		      $("#navigation-new").css("right", "-170px");
		});

		$(".text-wrap").click(function() {
					$("#close").css("display", "block");
		      $("#navigation-new").css("right", "150px");
		});

}


$(window).load(function(){
   $('div.main-content').css('padding-top', $('header>nav.navbar').outerHeight()+$('div.mini-header').height()-10);
});


$( ".validation" ).focusout(function() {
    textValue =  $.trim($(this).val());
    if(textValue ==''){
       $.trim($(this).val('')); //to set it blank
    } else {
       return true;
    }
});
