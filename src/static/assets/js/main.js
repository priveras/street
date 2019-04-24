$(function(){

  $('.delete-post').click(function(){
    var id = $(this).attr('data-id');
    $('#delete-post-submit').attr('data-id', id);
    console.log(id + 'hello');
  });

  $('#delete-post-submit').click(function(){
    var id = $(this).attr('data-id');
    var path = '/api/delete/post/' + id;

    $.post(path, function(data) {
      $('#delete1').modal('toggle');
      window.location.reload();
    });
  });

  $('.delete-comment').click(function(){
    var id = $(this).attr('data-id');
    $('#delete-comment-submit').attr('data-id', id);
    console.log(id + 'hello');
  });

  $('#delete-comment-submit').click(function(){
    var id = $(this).attr('data-id');
    var path = '/api/delete/comment/' + id;

    $.post(path, function(data) {
      $('#delete2').modal('toggle');
      window.location.reload();
    });
  });

  $('.delete-job').click(function(){
    var id = $(this).attr('data-id');
    $('#delete-job-submit').attr('data-id', id);
    console.log(id + 'hello');
  });

  $('#delete-job-submit').click(function(){
    var id = $(this).attr('data-id');
    var path = '/api/delete/job/' + id;

    $.post(path, function(data) {
      $('#delete3').modal('toggle');
      window.location.reload();
    });
  });

  $('.delete-event').click(function(){
    var id = $(this).attr('data-id');
    $('#delete-event-submit').attr('data-id', id);
    console.log(id + 'hello');
  });

  $('#delete-event-submit').click(function(){
    var id = $(this).attr('data-id');
    var path = '/api/delete/event/' + id;

    $.post(path, function(data) {
      $('#delete4').modal('toggle');
      window.location.reload();
    });
  });

  $('.delete-vendor').click(function(){
    var id = $(this).attr('data-id');
    $('#delete-vendor-submit').attr('data-id', id);
    console.log(id + 'hello');
  });

  $('#delete-vendor-submit').click(function(){
    var id = $(this).attr('data-id');
    var path = '/api/delete/vendor/' + id;

    $.post(path, function(data) {
      $('#delete5').modal('toggle');
      window.location.reload();
    });
  });

  //save a post
  $('#post-form').submit(function(e){
    var myEditor = document.querySelector('#text-post')
    e.preventDefault();
    var html = myEditor.children[0].innerHTML
    var data = {
      text: html,
    };
    console.log(html);

    if(!data.text){
      return false;
    }

    $.post('/post/create/', data, function(data, status){
      if(status != 'success'){
        //TODO: show toast
        return false;
      }

      $('#post').modal('toggle');
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