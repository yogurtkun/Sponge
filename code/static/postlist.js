var postlist = new Vue({
  el: '#postlist',
  data: {
    items: [
    {"postid": "1111", "category": "category1", "title": "1", "description": "2", "price": 3, "time": "2018-03-15", "like": true, "user":"user123", "location":"NY", "imageDir":"http://placehold.it/500x300"},
    {"postid": "2222", "category": "category2", "title": "1", "description": "2", "price": 3, "time": "2018-03-15", "like": true, "user":"user123", "location":"NJ", "imageDir":"http://placehold.it/500x300"},
    {"postid": "3333", "category": "category3", "title": "1", "description": "2", "price": 3, "time": "2018-03-15", "like": true, "user":"user123", "location":"NY", "imageDir":"http://placehold.it/500x300"},
    ],
    filter_items: 'null',
    filter_result: 'null',
    filter_result_len: 0,
    filter_buyer_items: 0,
    filter_seller_items: 0,
    filter_len : 0,
    filter_buyer_len : 0,
    filter_seller_len : 0,
    filter_price_sorting: 0,
    filter_loc: "0",
    filter_post_time: 0,
    filter_search: "",
    filter_is_apply: false,
    filter_category_index: "ALL",
    filter_post_type : "0",
    filter_offset : 0,
    currentPage: 1,
    go_page: null,
    ITEMS_PER_PAGE : 10,
  },
  mounted(){
    this.query_buyer_seller_post()
    this.check_init_filter()
    this.filter_center()
  },
  watch: {
    filter_price_sorting: function(){
      this.filter_center()
    },
    filter_loc: function(){
      this.filter_center()
    },
    filter_post_time: function(){
      this.filter_center()
    },
    filter_search: function(){
      this.filter_center()
    },
    items: function(){
      this.filter_center()
    },
    filter_category_index: function(){
      this.filter_center()
    },
    filter_post_type: function(){
      this.filter_center()
    },
    currentPage: function(){
      this.filter_paging()
    }
  },
  methods:{
    query_buyer_seller_post(){
      $.ajax({
      url: '/postlist/buyer',
      dataType: 'json',
      type: "POST",

      success: (json)=>{
          console.log(json);

          this.filter_buyer_items = json;
          this.filter_buyer_len = json.length
      },
      }).fail(function($xhr) {
          var data = $xhr.responseJSON;
          console.log(data);
      });
    $.ajax({
      url: '/postlist/seller',
      dataType: 'json',
      type: "POST",

      success: (json)=>{
          console.log(json);

          this.filter_seller_items = json;
          this.filter_seller_len = json.length

          /*The following code should be moved to form a independent function*/
          var filter_items = [];
          for(var i = 0; i < this.filter_buyer_len; i++){
            filter_items.push(this.filter_buyer_items[i])
          }

          for(var i = 0; i < this.filter_seller_len; i++){
            filter_items.push(this.filter_seller_items[i])
          }

          // Default sort the items with latest post.
          filter_items = this.sortWithTime(filter_items, filter_items.length)
          this.items = filter_items
          this.filter_items = filter_items
          this.filter_result = filter_items
          this.filter_len = filter_items.length

      },
      }).fail(function($xhr) {
          var data = $xhr.responseJSON;
          console.log(data);
      });
    },

    check_init_filter:function(){
      var urlParams = window.location.search.substr(1)
      
      var location_index = urlParams.indexOf("location");
      var category_index = urlParams.indexOf("category");
      if(location_index !== -1)
      {
        this.filter_loc = String(urlParams.substring(location_index + "location=".length, urlParams.length).replace(/%20/g, " "))
      }
      else if(category_index !== -1)
      {
        this.filter_category_index = String(urlParams.substring(category_index + "category=".length, urlParams.length).replace(/%20/g, " "))
      }

      console.log(this.filter_loc)
      console.log(this.filter_category_index)
    },

    reset_filter: function(){
      this.filter_price_sorting = 0
      this.filter_loc = "0"
      this.filter_post_time = 0
      this.filter_search = ""
      this.filter_post_type = "0"
    },

    filter_posts: function(filter_items, filter_search){
      return filter_items.filter((item) => {
        var matched = ""

        //var matched = item.title.match(/filter_search/i)
        matched = item.title.match(new RegExp(filter_search, "i"));

        items = filter_items
        for (var i = 0; i < items.length; i++){
          if(matched !== null){
            if(items[i].title == matched.input){
              return items[i]
            }
          }
        }
      })
    },

    filter_price: function(filter_items, filter_price_sorting){
      var items = filter_items
      var filter_items = []
      var new_index = []
      var price = []
      var price_with_index = []

      if(items === null || items === undefined){
        return items
      }

      for (var i = 0; i < items.length; i++){
        price_with_index.push((items[i].price))
      }

      if(filter_price_sorting == 0){
        return items
      }
      else if(filter_price_sorting == 1){
        price_with_index = this.sortWithIndeces(price_with_index, "ASC")
      }
      else if(filter_price_sorting == 2){
        price_with_index = this.sortWithIndeces(price_with_index, "DESC")
      }
      else{
        return items
      }

      new_index = price_with_index.sortIndices

      for (var i = 0; i < new_index.length; i++){
        filter_items.push((items[new_index[i]]))
      }

      return filter_items
    },

    filter_location: function(filter_items, location){
      var items = filter_items
      var filter_items = []

      if(location == "0")
      {
        return items
      }

      if(items === null || items === undefined){
        return items
      }

      // Only select the city.
      for (var i = 0; i < items.length; i++){
        if(items[i].location == location){
          filter_items.push(items[i])
        }
      }

      return filter_items
    },

    filter_time: function(filter_items, time){
      var items = filter_items
      var filter_items = []
      var post_dt = []
      var need_dt = 0

      if(time == "0")
      {
        return items
      }

      if(items === null || items === undefined){
        return items
      }


      var nowDate= new Date();
      if(time == 1){
        // Last 6 hours
        need_dt = new Date(nowDate.getFullYear(), nowDate.getMonth(),
                           nowDate.getDate(),nowDate.getHours() - 6,
                           nowDate.getMinutes(), nowDate.getSeconds());
      }
      else if(time == 2){
        // Last 24 hours
        need_dt = new Date(nowDate.getFullYear(), nowDate.getMonth(),
                           nowDate.getDate(),nowDate.getHours() - 24,
                           nowDate.getMinutes(), nowDate.getSeconds());
      }
      else if(time == 3){
        // Last 7 days
        need_dt = new Date(nowDate.getFullYear(), nowDate.getMonth(),
                           nowDate.getDate() - 7,nowDate.getHours(),
                           nowDate.getMinutes(), nowDate.getSeconds());
      }
      else if(time == 4){
        // Last 1 month
        need_dt = new Date(nowDate.getFullYear(), nowDate.getMonth() - 1,
                           nowDate.getDate(),nowDate.getHours(),
                           nowDate.getMinutes(), nowDate.getSeconds());
      }
      else if(time == 5){
        // Last 3 months
        need_dt = new Date(nowDate.getFullYear(), nowDate.getMonth() - 3,
                           nowDate.getDate(),nowDate.getHours(),
                           nowDate.getMinutes(), nowDate.getSeconds());
      }

      for (var i = 0; i < items.length; i++){
        if(new Date(items[i].time) >= need_dt){
          filter_items.push(items[i])
        }
      } 

      return filter_items
    },

    filter_category: function(filter_items, category){
      var items = filter_items
      var filter_items = []

      if(category == "ALL")
      {
        return items
      }

      if(items === null || items === undefined){
        return items
      }
      for (var i = 0; i < items.length; i++){
        if(items[i].category == category){
          filter_items.push(items[i])
        }
      }

      return filter_items
    },

    filter_type: function(filter_items, type){
      var items = filter_items
      var filter_items = []

      if(items === null || items === undefined){
        return items
      }

      if(type == "0"){
        for (var i = 0; i < items.length; i++){
          if(items[i].hasOwnProperty("sellerName")){
            filter_items.push(items[i])
          }
        }
      }
      else if(type == "1"){
        for (var i = 0; i < items.length; i++){
          if(items[i].hasOwnProperty("buyerName")){
            filter_items.push(items[i])
          }
        }
      }
      else{
        return items
      }

      return filter_items
    },

    set_category: function(category){
      this.filter_category_index = category   
    },

    set_location: function(location){
      this.filter_loc = location
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

    sortWithTime: function(filter_items, filter_len){
      var items = filter_items
      var filter_items = []
      var time_with_index = []
      var new_index

      if(items === null || items === undefined){
        return items
      }

      for(var i = 0; i < filter_len; i++){
        time_with_index.push(new Date(items[i].time))
      }

      time_with_index = this.sortWithIndeces(time_with_index, "DESC")

      new_index = time_with_index.sortIndices

      for (var i = 0; i < new_index.length; i++){
        filter_items.push((items[new_index[i]]))
      }

      return filter_items
    },


    addFavorite: function(postType, postId){

      for(var i = 0; i < this.items.length; i++)
      {
        if(this.items[i].postId === postId && this.items[i].favorite === false)
        {
          this.items[i].favorite = true
        }
      }

      tdata = {"postType": postType, 'postId': postId}
      $.ajax({
          url: '/favorite',
          type: 'POST',
          data: tdata,
          success: (data) => {
          }
      })
    },

    deleteFavorite: function(postType, postId){

      for(var i = 0; i < this.items.length; i++)
      {
        if(this.items[i].postId === postId && this.items[i].favorite === true)
        {
          this.items[i].favorite = false
        }
      }

      tdata = {"postType": postType, 'postId': postId}
      $.ajax({
          url: '/deleteFavorite',
          type: 'POST',
          data: tdata,
          success: (data) => {
          }
      })
    },

    _remove_ordered_item: function(filter_items){
      var items = filter_items
      var filter_items = []

      if(items === null || items === undefined){
        return items
      }

      for (var i = 0; i < items.length; i++){
        if(items[i].order == false){
          filter_items.push(items[i])
        }
      }

      return filter_items
    },

    filter_paging: function(){
      var filter_items = []
      var filter_len = 0
      var start_idx = (this.currentPage - 1)* this.ITEMS_PER_PAGE
      var end_idx = (this.currentPage) * this.ITEMS_PER_PAGE
      var total_length = this.filter_result.length

      for(var i = start_idx; i < end_idx; i++)
      {
        if((total_length - i - 1) < 0)
        {
          break
        }
        filter_items.push(this.filter_result[i])
        filter_len ++;
      }

      this.filter_items = filter_items
      this.filter_len = filter_len

      this.jump_to_top()
    },

    jump_to_page:function(){
      console.log(this.go_page)
      console.log(parseInt(this.go_page))
      console.log(typeof(parseInt(this.go_page)))
      if(this.go_page !== null)
      {
        this.currentPage = parseInt(this.go_page)
      }
    },

    jump_to_top: function() {
      $('html,body').stop().animate({
        scrollTop: 0
      }, 'slow', 'swing');
    },

    filter_center: function(){
      var filter_items = this.items
      var filter_price_sorting = this.filter_price_sorting
      var filter_loc = this.filter_loc
      var filter_post_time = this.filter_post_time
      var filter_search = this.filter_search
      var filter_search_items = []
      var filter_type = this.filter_post_type
      var filter_category = this.filter_category_index

      if(filter_price_sorting == 0 && filter_loc == "0" &&
        filter_post_time == 0 && filter_category == "all"){
        filter_items = this.sortWithTime(filter_items, filter_items.length)
        //filter_items = this._remove_ordered_item(filter_items)
      }
      else{
        filter_items = this.filter_price(filter_items, filter_price_sorting)
        filter_items = this.filter_location(filter_items, filter_loc)
        filter_items = this.filter_time(filter_items, filter_post_time)
        filter_items = this.filter_category(filter_items, filter_category)
        filter_items = this.filter_type(filter_items, filter_type)
        //filter_items = this._remove_ordered_item(filter_items)
      }

      filter_search_items.push(this.filter_posts(filter_items, filter_search))
      
      //this.filter_items = filter_search_items[0]
      //this.filter_len = filter_search_items[0].length
      this.filter_result = filter_search_items[0]
      this.filter_result_len = filter_search_items[0].length
      this.filter_paging()
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
