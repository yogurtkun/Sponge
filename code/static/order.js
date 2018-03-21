$(document).ready(function () {
    var checkoutInfo = new Vue({
        el: '#checkoutform',
        data: {
            rcvAddress: "",
            transactionType: ""
        },
        created() {
            $.ajax({
                url: '/userinfo',
                type: 'POST',
                success: (data) => {
                    retUser = JSON.parse(data);
                    console.log(retUser);

                    this.rcvAddress = retUser.address;
                }
            });
        },
        methods: {
            checkout: function () {
                tdata = { 
                    "rcvAddress": this.rcvAddress, "transactionType": this.transactionType,
                    "postId": $("#item-postid").val()
                };
                console.log(tdata);
                $.ajax({
                    url: '/checkout',
                    type: 'POST',
                    data: tdata,
                    success: (data) => {
                        console.log("success!")
                    }
                })
            },
            checkType: function () {
                if (this.transactionType === "Face to Face") {
                    $('#addressmayhide').hide();
                } else {
                    $('#addressmayhide').show();
                }
            }
        }
    });
});