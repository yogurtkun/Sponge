$(document).ready(function(){
  $("#favoriteBtn").attr('class', 'visible');

  var checkVue = new Vue({
    el:"#checkbutton",
    methods: {
      checkout: function(){
        var urlParams = new URLSearchParams(window.location.search);
        var postId = urlParams.get("postId");
        window.location.href = "/buyorder?postId="+postId;
      }
    }
  });

  var favoriteBtn = new Vue({
  el: "#favoriteBtn",
  data: {
    is_favorite : undefined
  },
  methods:{
    deleteFavorite : function(postType, postId){
      console.log("delete")
      console.log(postType, postId)
      this.is_favorite = false
      console.log(this.is_favorite)

      tdata = {"postType": postType, 'postId': postId}
      console.log("delete", tdata);
      $.ajax({
          url: '/deleteFavorite',
          type: 'POST',
          data: tdata,
          success: (data) => {
              console.log("success!")
              this.query_buyer_seller_post()
          }
      })
    },

    addFavorite : function(postType, postId){
      console.log("add")
      console.log(postType, postId)
      this.is_favorite = true
      console.log(this.is_favorite)

      tdata = {"postType": postType, 'postId': postId}
      console.log("add", tdata);
      $.ajax({
          url: '/favorite',
          type: 'POST',
          data: tdata,
          success: (data) => {
              console.log("success!")
              this.query_buyer_seller_post()
          }
        })
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