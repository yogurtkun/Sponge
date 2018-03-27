
    var userinfo = new Vue({
        el: '#user-info',
        data: {
            reviews : "null",
            orders : "null",
        },
        created(){
            var usr_text = $("#user-name").text().replace(/ /g,'');
            var index = usr_text.indexOf("User")
            var username = usr_text.substr(index+5, usr_text.length-index-1-5)
            var tdata = {"username" : username}

            $.ajax({
            url: '/getOrdersToUser',
            type: 'POST',
            data: tdata,
            success: (data) => {
                json = JSON.parse(data)
                console.log(json)

                this.orders = json
            },
            }).fail(function($xhr) {
              var data = $xhr.responseJSON;
              console.log(data);
            });
        },

        methods:{
            add_review_post: function(){
                var tdata = {"reviewee" : 'zcd', rating:4, 'content':"testreview testreview testreview testreview", 'orderId': 123}

                $.ajax({
                url: '/addReview',
                type: 'POST',
                data: tdata,
                success: (data) => {
                    json = JSON.parse(data)
                    console.log(json)

                    this.reviews = json
                },
                }).fail(function($xhr) {
                  var data = $xhr.responseJSON;
                  console.log(data);
                });
            },

            query_review_info: function(){
                var usr_text = $("#user-name").text().replace(/ /g,'');
                var index = usr_text.indexOf("User")
                var username = usr_text.substr(index+5, usr_text.length-index-1-5)
                var tdata = {"username" : username}

                $.ajax({
                url: '/getReviewsToUser',
                type: 'POST',
                data: tdata,
                success: (data) => {
                    json = JSON.parse(data)
                    console.log(json)

                    this.reviews = json
                },
                }).fail(function($xhr) {
                  var data = $xhr.responseJSON;
                  console.log(data);
                });
            }
        }
    });

