
var userinfo = new Vue({
    el: '#user-info',
    data: {
        reviews : "null",
        on_sell_items : "null",
        in_need_items : "null",

        all_reviews : "null",
        all_selling_items : "null",
        all_buying_items : "null",
        check_username : "null",
    },
    created(){

      $.ajax({
      url: '/postlist/seller',
      dataType: 'json',
      type: "POST",

      success: (json)=>{
          console.log(json);

          this.all_selling_items = json;

          this.check_username = this.get_check_username()
          this.on_sell_items = this.get_on_sell_items(this.all_selling_items, this.check_username)
          this.on_sell_items = this.sortWithTime(this.on_sell_items, this.on_sell_items.length)
          this.on_sell_items = this._remove_ordered_item(this.on_sell_items)

          if(this.on_sell_items !== undefined)
          {
            if(this.on_sell_items.length === 0)
            {
              this.on_sell_items = "None"
            }
          }
      },
      }).fail(function($xhr) {
          var data = $xhr.responseJSON;
          console.log(data);
      });
    },

    methods:{
        get_check_username: function(){
            var usr_text = $("#user-name").text().replace(/ /g,'');
            var username = usr_text
            this.check_username = username

            return username
        },

        query_in_need_info: function(){
            $.ajax({
              url: '/postlist/buyer',
              dataType: 'json',
              type: "POST",

              success: (json)=>{
                  console.log(json);
                  this.all_buying_items = json

                  this.check_username = this.get_check_username()
                  this.in_need_items = this.get_in_need_items(this.all_buying_items, this.check_username)
                  this.in_need_items = this.sortWithTime(this.in_need_items, this.in_need_items.length)
                  this.in_need_items = this._remove_ordered_item(this.in_need_items)
             
                  if(this.in_need_items !== undefined)
                  {
                    if(this.in_need_items.length == 0)
                    {
                      this.in_need_items = "None"
                    }
                  }
              },
              }).fail(function($xhr) {
                  var data = $xhr.responseJSON;
                  console.log(data);
              });
        },

        query_review_info: function(){
            var usr_text = $("#user-name").text().replace(/ /g,'');
            var username = usr_text
            var tdata = {"username" : username}

            $.ajax({
            url: '/getReviewsToUser',
            type: 'POST',
            data: tdata,
            success: (data) => {
                json = JSON.parse(data)
                console.log(json)

                this.all_reviews = json
                this.reviews = this.sortWithTime(this.all_reviews, this.all_reviews.length)
            },
            }).fail(function($xhr) {
              var data = $xhr.responseJSON;
              console.log(data);
            });
        },

        get_on_sell_items: function(all_selling_items, username){
            var username = username
            var all_selling_items = all_selling_items
            var on_sell_items = []

            for(var i = 0; i < all_selling_items.length; i++)
            {
                if(all_selling_items[i].sellerName == username)
                {
                    on_sell_items.push(all_selling_items[i])
                }
            }

            return on_sell_items
        },

        get_in_need_items: function(all_in_need_items, username){
            var username = username
            var all_in_need_items = all_in_need_items
            var in_need_items = []

            for(var i = 0; i < all_in_need_items.length; i++)
            {
                if(all_in_need_items[i].buyerName == username)
                {
                    in_need_items.push(all_in_need_items[i])
                }
            }

            return in_need_items
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
    }
});

