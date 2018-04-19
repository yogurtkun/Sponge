
    var checkoutInfo = new Vue({
        el: '#checkoutform',
        data: {
            errors: [],
            rcvAddress: {
                ad1: "",
                ad2: "",
                city: "",
                state: ""
            },
            transactionType: "",
            ifCheck: false
        },
        created() {
            $.ajax({
                url: '/userinfo',
                type: 'POST',
                success: (data) => {
                    retUser = JSON.parse(data);
                    if (retUser.address !== null) {
                        newAddress = JSON.parse(retUser.address);
                        this.rcvAddress = newAddress;
                    }
                    this.transactionType="Online";
                }
            });
        },
        watch:{
            transactionType: function(){
                if(this.transactionType === "Face to Face"){
                    this.errors = [];
                }
            }
        },
        methods: {
            checkform: function () {
                if(this.transactionType === "Face to Face"){
                    return true;
                }

                let ispass = true;
                if (this.transactionType === "") {
                    this.errors.push("Transaction Type Required")
                    ispass = false;
                };

                if (this.rcvAddress.ad1 === "") {
                    this.errors.push("Address Required");
                    ispass = false;
                }

                if (this.rcvAddress.city === "") {
                    this.errors.push("City Required");
                    ispass = false;
                }
                
                console.log(this.rcvAddress.state)
                if (this.rcvAddress.state === "" || typeof this.rcvAddress.state === 'undefined') {
                    this.errors.push("State Required");
                    ispass = false;
                }
                return ispass;
            },
            checkout: function () {
                stringAddress = JSON.stringify(this.rcvAddress);
                var urlParams = new URLSearchParams(window.location.search);
                var postId = urlParams.get("postId");
                tdata = {
                    "rcvAddress": stringAddress,
                    "transactionType": this.transactionType,
                    "postId": postId
                };
                console.log(tdata);
                $.ajax({
                    url: '/checkout',
                    type: 'POST',
                    data: tdata,
                    success: (data) => {
                        if (data !== "Placing order failed!") {
                            window.location = "/portal?section=order"
                        }
                    }
                })
            },
            confirm: function () {
                var self = this;
                self.$nextTick(function () {
                    self.errors=[];
                    if (!self.checkform() ) {
                        console.log(this.errors);
                        return;
                    }
                    self.ifCheck = true;
                });
            },
            review: function(){
                var self = this;
                self.$nextTick(function(){
                    self.ifCheck = false;
                });
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
