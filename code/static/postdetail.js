var postdetail = new Vue({
  el: '#post-info',
  data: {
    post_title: "title",
    post_user: "anonymous",
    post_time: "2018-01-01",
    post_image_src: ["http://placehold.it/900x300", "http://placehold.it/900x300"],
    post_description: "Add post description",
  },
  created(){
    $.ajax({
      url: '/testPostDetail',
      dataType: 'json',
      type: "POST",

      success: (json)=>{
          console.log(json);
          this.post_title = json.data.title;
          this.post_user = json.data.user;
          this.post_time = json.data.time;
          this.post_image_src = json.data.imageDir;
          this.post_description = json.data.description;
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

var sidebar = new Vue({
  el: '#sidebars',
  data: {
    post_user: "anonymous",
  },
  created(){
    $.ajax({
      url: '/testPostDetail',
      dataType: 'json',
      type: "POST",

      success: (json)=>{
          console.log(json);
          this.post_user = json.data.user;
      },
      }).fail(function($xhr) {
          var data = $xhr.responseJSON;
          console.log(data);
      });
  },
});