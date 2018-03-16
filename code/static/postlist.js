Vue.component('postitems', {
  props: 
  {
    postid:
    {
      type: String,
      required: true
    },
    title: 
    {
      type: String,
      required: true
    },
    category:
    {
      type: String,
      required: true
    },
    description: 
    {
      type: String,
      required: true
    },
    price: 
    {
      type: Number,
    },
    time: 
    {
      type: String,
      required: true
    },
    like: 
    {
      type: Boolean,
      required: true
    },
    user:
    {
      type: String,
      required: true
    },
    location:
    {
      type: String,
      required: true
    },
    imageDir:
    {
      type: String,
    }
  },
  template: `<div class="card mt-2">
              <div class="row">
                <div class="col">
                  <p class="card-text">
                    <div class="product_image2">
                      <a v-bind:href="postid"><img src="https://bit.ly/1myplK1" alt=""></a>
                      <div class="product_buttons">
                        <button class="product_heart"><i class="fa fa-heart"></i></button>
                        <button class="add_to_cart"><i class="fa fa-shopping-cart"></i></button>
                      </div>
                    </div>
                  </p>
                </div>
                <div class="col-8">
                  <div>
                    <h2>
                      <a class="card-title" v-bind:href="postid">
                        {{title}}
                      </a>
                    </h2>
                    <p class="card-text">
                      {{description}}
                    </p>
                  </div>
                </div>
                <div class="col">
                  <h5 class="text-danger float-right">
                    \${{price}}
                  </h5>
                </div>
              </div>
              <p class="card-footer text-muted text-center">
                <span class="float-left">Category:{{category}}</span> 
                <span class="text-center">Location:{{location}} </span> 
                <span class="float-right">{{user}} posted on {{time}}</span>
              </p>
            </div>`
  /*Template candiate
    template:`<li class="product_item">
              <div class="product_image">
                <a v-bind:href="postid"><img src="https://bit.ly/1myplK1" alt=""></a>
                  <div class="product_buttons">
                    <button class="product_heart"><i class="fa fa-heart"></i></button>
                    <button class="add_to_cart"><i class="fa fa-shopping-cart"></i></button>
                  </div>
              </div>
              <div class="product_values">
                <div class="product_title">
                  <h3>{{title}}</h3>
                </div>
                <div class="product_price">
                  <div href="#"><span class="price_old">old_price</span> <span class="price_new">{{price}}</span></div>
                </div>
                <div class="product_desc">
                  <p class="truncate">{{description}}</p>
                </div>
              </div>
            <li>`*/
});

Vue.component('category', {
  props: 
  {
    category:
    {
      type: String,
      required: true
    },
  },
  template: '<a v-bind:href="category">{{category}}</a>'
});

var items = new Vue({
  el: '#postitem',
  data: {
    items: [
    {"postid": "1111", "category": "ca1", "title": "1", "description": "2", "price": 3, "time": "2018-03-15", "like": true, "user":"user123", "location":"NY", "imageDir":"static/test.jpg"},
    {"postid": "2222", "category": "ca1", "title": "1", "description": "2", "price": 3, "time": "2018-03-15", "like": true, "user":"user123", "location":"NY", "imageDir":"static/test.jpg"},
    {"postid": "3333", "category": "ca1", "title": "1", "description": "2", "price": 3, "time": "2018-03-15", "like": true, "user":"user123", "location":"NY", "imageDir":"static/test.jpg"},
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

var category = new Vue({
  el: '#category',
  data: {
    category: [
    {"category": "ca1"},
    {"category": "ca2"},
    {"category": "ca3"},
    ]
  },
  created(){
    $.ajax({
      url: '/testCategory',
      dataType: 'json',
      type: "POST",

      success: (json)=>{
          console.log(json);
          this.category = json.data;
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
