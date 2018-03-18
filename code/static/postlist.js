var postlist = new Vue({
  el: '#postlist',
  data: {
    items: [
    {"postid": "1111", "category": "category1", "title": "1", "description": "2", "price": 3, "time": "2018-03-15", "like": true, "user":"user123", "location":"NY", "imageDir":"http://placehold.it/500x300"},
    {"postid": "2222", "category": "category2", "title": "1", "description": "2", "price": 3, "time": "2018-03-15", "like": true, "user":"user123", "location":"NY", "imageDir":"http://placehold.it/500x300"},
    {"postid": "3333", "category": "category3", "title": "1", "description": "2", "price": 3, "time": "2018-03-15", "like": true, "user":"user123", "location":"NY", "imageDir":"http://placehold.it/500x300"},
    ],
    filter_items: 0,
    filter_price_sorting: 0,
    filter_location: "0",
    filter_post_time: 0,
    filter_search: "",
    filter_is_apply: false,
    filter_btn_color: "btn btn-info",
    filter_btn_context: "Apply",
  },
  created(){
    $.ajax({
      url: '/postlist/seller',
      dataType: 'json',
      type: "POST",

      success: (json)=>{
          console.log(json);
          this.items = json;
          this.filter_items = json;
      },
      }).fail(function($xhr) {
          var data = $xhr.responseJSON;
          console.log(data);
      });
  },
  methods:{
    apply_filter: function(event){
      this.filter_is_apply = !this.filter_is_apply
      if(this.filter_is_apply === true){
        this.filter_btn_color = "btn btn-primary"
        this.filter_btn_context = "Reset"
      }
      else{
        this.filter_btn_color = "btn btn-info"
        this.filter_btn_context = "Apply"
      }

      console.log(this.filter_price_sorting)
      console.log(this.filter_location)
      console.log(this.filter_post_time)
      console.log(this.filter_search)
      if(this.filter_price_sorting === 0 && this.filter_location === "0" &&
         this.filter_post_time === 0 && this.filter_search === ""){
        console.log("nothing needs to filter \n")
        return 0
      }

      // Seach filter
      filter_items = []
      filter_items.push(this.filter_posts())
      this.filter_items = filter_items[0]

      // Price filter
      if(this.filter_price_sorting == 1){
        this.filter_price("ASC")
      }
      else if(this.filter_price_sorting == 2){
        this.filter_price("DESC")
      }
    },

    filter_posts: function(){
      return this.items.filter((item) => {
        var matched = item.title.match(this.filter_search)
        items = this.items
        for (var i = 0; i < items.length; i++){
          if(matched !== null){
            if(items[i].title == matched.input){
              return items[i]
            }
          }
        }
      })
    },
    filter_price: function(order){
      var items = this.filter_items
      var filter_items = []
      var new_index = []
      var price = []
      var price_with_index = []
      for (var i = 0; i < items.length; i++){
        price_with_index.push((items[i].price))
      }

      price_with_index = this.sortWithIndeces(price_with_index, order)
      new_index = price_with_index.sortIndices

      for (var i = 0; i < new_index.length; i++){
        filter_items.push((items[new_index[i]]))
      }

      this.filter_items = filter_items
    },

    sortWithIndeces: function(toSort, order) {
      for (var i = 0; i < toSort.length; i++) {
        toSort[i] = [toSort[i], i];
      }

      if(order == "ASC"){
        toSort.sort(function(left, right) {
          return left[0] < right[0] ? -1 : 1;
        });
      }
      else if(order == "DESC"){
        toSort.sort(function(left, right) {
          return left[0] > right[0] ? -1 : 1;
        });
      }

      toSort.sortIndices = [];
      for (var j = 0; j < toSort.length; j++) {
        toSort.sortIndices.push(toSort[j][1]);
        toSort[j] = toSort[j][0];
      }
      return toSort;
    },
  }
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
