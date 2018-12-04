$(function(){

  //save a post
  $('#post-form').submit(function(e){
    e.preventDefault();
    var data = {
      text: $('#text-post').val(),
      company: $('#company-post').val(),
      image: $('#image-post').val(),
    };

    if(!data.text){
      return false;
    }

    $.post('/post/create/', data, function(data, status){
      if(status != 'success'){
        //TODO: show toast
        return false;
      }

      $('#text-post').val("");
      $('#post-divider').after(data);
    });

    return false;
  });

  $('.comment-submit').on('click', function(){
    var form = $(this).parents('form');
    save_comment(form);
  });

  //save a comment
  $('.comment-form').submit(function(e){
    e.preventDefault();
    var form = $(this);
    save_comment(form);
    return false;
  });

  function save_comment(form){
    data = {
      text: form.find('.comment-text').val(),
      post: form.attr('data-postid')
    };

    if(!data.text){
      return;
    }

    form.find('.comment-text').val("");

    $.post('/post/comment/create/', data, function(data, status){
      if(status != 'success'){
        //TODO: show toast
        return
      }

      $('#post_'+form.attr('data-postid')).append(data);
    });
  }

});