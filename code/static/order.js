$(document).ready(function () {
    var checkoutInfo = new Vue({
        el: '#checkoutform',
        data: {
            errors: [],
            rcvAddress: {
                ad1: "",
                ad2: "",
                city: "",
                region: "",
                country: ""
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
                }
            });
        },
        methods: {
            checkform: function () {
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

                if (this.rcvAddress.country === "") {
                    this.errors.push("Country Required");
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
                        if (data === "Placeing order succeeded!") {
                            window.location = "/portal"
                        }
                    }
                })
            },
            confirm: function () {
                var self = this;
                self.$nextTick(function () {
                    self.errors=[];
                    if (!self.checkform()) {
                        console.log(this.errors);
                        return;
                    }
                    self.ifCheck = true;
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
});