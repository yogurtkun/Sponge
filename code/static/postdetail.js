$(document).ready(function(){
  var checkVue = new Vue({
    el:"#checkbutton",
    methods: {
      checkout: function(){
        var urlParams =new URLSearchParams(window.location.search);
        var postId = urlParams.get("postId");
        window.location.href = "/buyorder?postId="+postId;
      }
    }
  });
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