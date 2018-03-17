var items = new Vue({
  el: '#postitem',
  data: {
    items: [
    {"postid": "1111", "category": "category1", "title": "1", "description": "2", "price": 3, "time": "2018-03-15", "like": true, "user":"user123", "location":"NY", "imageDir":"http://placehold.it/500x300"},
    {"postid": "2222", "category": "category2", "title": "1", "description": "2", "price": 3, "time": "2018-03-15", "like": true, "user":"user123", "location":"NY", "imageDir":"http://placehold.it/500x300"},
    {"postid": "3333", "category": "category3", "title": "1", "description": "2", "price": 3, "time": "2018-03-15", "like": true, "user":"user123", "location":"NY", "imageDir":"http://placehold.it/500x300"},
    ]
  },
  created(){
    $.ajax({
      url: '/testPostList',
      dataType: 'json',
      type: "POST",

      success: (json)=>{
          console.log(json);
          this.items = json.data;
      },
      }).fail(function($xhr) {
          var data = $xhr.responseJSON;
          console.log(data);
      });
  },
});

/*Move to Top Button*/
Vue.component('backtotop', {
  template: '#backtotop',
  data: function() {
    return {
      isVisible: false
    };
  },
  methods: {
    initToTopButton: function() {
      $(document).bind('scroll', function() {
        var backToTopButton = $('.goTop');
        if ($(document).scrollTop() > 250) {
          backToTopButton.addClass('isVisible');
          this.isVisible = true;
        } else {
          backToTopButton.removeClass('isVisible');
          this.isVisible = false;
        }
      }.bind(this));
    },
    backToTop: function() {
      $('html,body').stop().animate({
        scrollTop: 0
      }, 'slow', 'swing');
    }
  },
  mounted: function() {
    this.$nextTick(function() {
      this.initToTopButton();
    });
  }
});

var app = new Vue({
  el: '#toTop'
});
