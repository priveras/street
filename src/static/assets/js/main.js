$ = jQuery;
$(function(){
  $('.btn-success.float-right').click(function(){
    var id = $('.nav-link.active').attr('data-id');
    var number = id.replace('nav-','');
    var next = +number + 1;
    var next_item = 'nav-'+next;
    $('a[data-id="'+next_item+'"]').click();
    $("html, body").animate({ scrollTop: 0 }, "fast");
  });
  $('.btn-success.left').click(function(){
    var id = $('.nav-link.active').attr('data-id');
    var number = id.replace('nav-','');
    var next = +number -1;
    var next_item = 'nav-'+next;
    $('a[data-id="'+next_item+'"]').click();
    $("html, body").animate({ scrollTop: 0 }, "fast");
  });
});
