$(document).ready(function () {
    var postInfo = new Vue({
        el: '.order-confirmation',
        data: {
            item: {
                title: "",
                sellername: "",
                description: "",
                price: ""
            }
        },
        created() {
            $.ajax({
                url: 'BuyerPost',
                dataType: 'json',
                type: 'GET',
                success: (data) => {
                    this.item = data;
                }
            })
        }
    });
})

$(document).ready(function () {
    var checkoutInfo = new Vue({
        el: '#checkoutform',
        data:{
            sendAddress: "",
            transactionType: ""
        },
        created(){
            $.ajax({
                url: '/userinfo',
                type: 'POST',
                success: (data) => {
                    retUser = JSON.parse(data);

                    this.sendAddress = retUser.address;
                }
            });
        },
        methods:{
            checkout: function(){
                tdata={"sendAddress":this.sendAddress,"transactionType":this.transactionType};
                console.log(tdata);
                $.ajax({
                    url:'/checkout',
                    type:'POST',
                    data:tdata,
                    success:(data)=>{
                        console.log("success!")
                    }
                })
            },
            checkType: function(){
                if(this.transactionType === "Face to Face"){
                    $('#addressmayhide').hide();
                }else{
                    $('#addressmayhide').show();
                }
            }
        }
    });
});