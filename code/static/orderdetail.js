var userinfo = new Vue({
    el: '#buttons',
    data: {
        review: undefined,
        rating: 0,
        reviewee: 'null',
        orderId: undefined,
        review_submit: false,
        trackNo: undefined,
        carrier: undefined,
        ship_submit: false,
        text_max: 150,
        text_length: 0,
    },
    watch: {
        // whenever question changes, this function will run
        review: function () {
          this.text_length = this.review.length
        }
    },
    methods: {
        get_reviewee: function(){
            var reviewee_text = $("#seller").text().replace(/ /g,'');
            var reviewee = reviewee_text.substring(reviewee_text.indexOf(':')+1, reviewee_text.length-1)
            
            return reviewee
        },

        get_order_id: function(){
            var href = window.location.href;
            var orderId = href.substr(href.indexOf("orderId")+8, 9)

            return orderId  
        },

        AddReview:function(){
            console.log('AddReview')
            this.reviewee = this.get_reviewee()
            this.orderId = this.get_order_id()

            var tdata = {'reviewee':this.reviewee, 'rating':this.rating,
                         'content':this.review, 'orderId':this.orderId}

            this.review_submit = true

            $.ajax({
            url: '/addReview',
            type: 'POST',
            data: tdata,
            dataType : 'json',
            success: (data) => {
                this.updateOrderStatus('Completed')
            },
            }).fail(function($xhr) {
              var data = $xhr.responseJSON;
            });

        },

        ShipOrder:function(){
            console.log('ShipOrder')
            this.orderId = this.get_order_id()

            var tdata = {'carrier':this.carrier, 'trackNo':this.trackNo, 'orderId':this.orderId}

            this.ship_submit = true

            $.ajax({
            url: '/shipOrder',
            type: 'POST',
            data: tdata,
            dataType : 'json',
            success: (data) => {
                console.log(data);
                if (data === "succeeded") {
                    this.updateOrderStatus('Shipped');
                }
            },
            }).fail(function($xhr) {
              var data = $xhr.responseJSON;
            });

        },

        updateOrderStatus : function(nextStatus) {
            console.log('update order status')
            var orderId = this.get_order_id();
            var udata = {'orderId': orderId, 'status': nextStatus}
            $.ajax({
                url: '/updateOrderStatus',
                type: 'POST',
                data: udata,
                dataType: 'json',
                success: (data) => {
                    window.location.reload(true);
                }
            }).fail(function($xhr) {
                var data = $xhr.responseJSON;
            });
        },

        cancelOrder: function(){
            console.log('cancel order')
            var orderId = this.get_order_id();
            var udata = {'orderId': orderId}
            $.ajax({
                url: '/cancelOrder',
                type: 'POST',
                data: udata,
                dataType: 'json',
                success: (data) => {
                    console.log(data);
                    if (data === "Succeeded!") {
                        alert('Order is canceled!');
                        window.location.href = "/";
                    }
                }
            }).fail(function($xhr) {
                var data = $xhr.responseJSON;
            });
        },
    },
});

