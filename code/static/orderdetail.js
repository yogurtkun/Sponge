$(document).ready(() => {
    var text_max = 200;
    $('#count_message').html('0 / ' + text_max );

    $('#text').keyup(function() {
      var text_length = $('#text').val().length;
      var text_remaining = text_max - text_length;
      
      $('#count_message').html(text_length + ' / ' + text_max);
    });

    var userinfo = new Vue({
        el: '#completeBtn',
        data: {
        },
        methods: {
            AddReview:function(){

            },
        },
    });
});