function tobottom(){
    console.log("hello")
    $(".messages").animate({ scrollTop: getMessageHeight() }, "fast");
}

$(document).ready(() => {
    var userinfo = new Vue({
        el: '#user-info',
        data: {
            user: {
                'username': "Empty",
                "email": "Empty",
                "zipcode": "Empty",
                "phoneNumber": "Empty",
                "address": "Empty"
            },
            myaddress: {
                "ad1": "",
                "ad2": "",
                "city": "",
                "region": "",
                "country": ""
            }
        },
        methods: {
            changeInfo: function () {
                this.user.address = JSON.stringify(this.myaddress)

                $.ajax({
                    url: '/updateUser',
                    type: 'POST',
                    data: this.user,
                    success: (data) => {
                        if (data === "Success") {
                            alert("Save Successfully");
                        } else {
                            alert("Save Failed");
                        }
                    }
                });
            }
        },
        created() {
            $.ajax({
                url: '/userinfo',
                type: 'POST',
                success: (data) => {
                    retUser = JSON.parse(data)
                    this.user = Object.assign({}, retUser);

                    if (this.user.address !== null) {
                        let tempaddr = JSON.parse(this.user.address);
                        this.myaddress = tempaddr
                    }

                    for (let k in this.user) {
                        if (this.user[k] === "" || this.user[k] === null) {
                            this.user[k] = "";
                        }
                    }
                }
            });
        }
    });
});

// $(document).ready(function(){
//     var newChat = new Vue({
//         el: "#newMessageCreate",
//         methods:{
//             newchat: function(){
//                 var inputuser = $("#new-user").val();
//                 window.location.replace("/messages?person="+inputuser);
//             }
//         }
//     });
// });

$(document).ready(function () {
    $('#favorite-table').bootstrapTable({
        url: "/favoriteList",
        method: 'POST',
        sidePagination: "client",
        pagination: true,
        sortName: "time",
        sortOrder: "desc",
        search: true,
        pageSize: 10,
        strictSearch: false,
        columns: [
            {
                title: 'Post Id',
                field: 'postId',
                align: 'center',
                valign: 'middle',
                width: '10%',
                sortable: true,
                formatter: function (value, row, index) {
                    if (row['type'] === "Buyer") {
                        return '<a href="/BuyerPost?postId=' + value + '">' + value + '</a>';
                    }else{
                        return '<a href="/SellerPost?postId=' + value + '">' + value + '</a>';
                    }
                }
            },
            {
                title: 'Title',
                field: 'title',
                align: 'center',
                valign: 'middle',
                width: '20%',
                sortable: true
            },
            {
                title: 'Price',
                field: 'price',
                align: 'center',
                valign: 'middle',
                width: '20%',
                sortable: true
            },
            {
                title: 'Type',
                field: 'type',
                align: 'center',
                valign: 'middle',
                width: '20%',
                formatter: function(value,row,index){
                    if(row['type'] === 'Seller'){
                        return "Sell";
                    }else{
                        return "Buy";
                    }
                }
            },
            {
                title: 'Time',
                field: 'time',
                align: 'center',
                valign: 'middle',
                width: '20%',
                sortable: true
            },
            {
                title: 'Like',
                align: 'center',
                valign: 'middle',
                width: '10%',
                formatter: function(value,row,index){
                    return '<a id="like-delete"><i class="fas fa-trash-alt"></i></a>'
                },
                events:{
                    'click #like-delete':function(e,value,row,index){
                        mess={
                            "postType":row['type'],
                            "postId":row['postId']
                        };
                        $.ajax({
                            url: "/deleteFavorite",
                            data: mess,
                            type: 'POST',
                            dataType:'json',
                            success: function (ret) {
                                console.log("ret")
                                window.location.replace("/portal?section=favorite") 
                            },
                            fail:function(){
                                console.log("!!!!")
                            }
                        });
                        window.location.replace("/portal?section=favorite") 
                    }
                }
            }
        ]
    });
})

$(document).ready(function () {
    $('#buy-post-table').bootstrapTable({
        url: "/buypostlist",
        method: 'POST',
        sidePagination: "client",
        pagination: true,
        sortName: "postId",
        search: true,
        pageSize: 10,
        strictSearch: false,
        columns: [
            {
                title: 'Post Id',
                field: 'postId',
                align: 'center',
                valign: 'middle',
                width: '20%',
                formatter: function (value, row, index) {
                    return '<a href="/BuyerPost?postId=' + value + '">' + value + '</a>';
                }
            },
            {
                title: 'Title',
                field: 'title',
                align: 'center',
                valign: 'middle',
                width: '20%'
            },
            {
                title: 'Category',
                field: 'category',
                align: 'center',
                valign: 'middle',
                width: '20%'
            },
            {
                title: 'Price',
                field: 'price',
                align: 'center',
                valign: 'middle',
                width: '20%',
                sortable: true
            },
            {
                title: 'Time',
                field: 'time',
                align: 'center',
                valign: 'middle',
                width: '20%',
                sortable: true
            }
        ]
    });
});

$(document).ready(function () {
    $('#sell-post-table').bootstrapTable({
        url: "/sellpostlist",
        method: 'POST',
        sidePagination: "client",
        pagination: true,
        sortName: "postId",
        search: true,
        pageSize: 10,
        strictSearch: false,
        columns: [
            {
                title: 'Post Id',
                field: 'postId',
                align: 'center',
                valign: 'middle',
                width: '20%',
                formatter: function (value, row, index) {
                    return '<a href="/SellerPost?postId=' + value + '">' + value + '</a>';
                }
            },
            {
                title: 'Title',
                field: 'title',
                align: 'center',
                valign: 'middle',
                width: '20%'
            },
            {
                title: 'Category',
                field: 'category',
                align: 'center',
                valign: 'middle',
                width: '20%'
            },
            {
                title: 'Price',
                field: 'price',
                align: 'center',
                valign: 'middle',
                width: '20%',
                sortable: true
            },
            {
                title: 'Time',
                field: 'time',
                align: 'center',
                valign: 'middle',
                width: '20%',
                sortable: true
            }
        ]
    });
})

$(document).ready(function () {
    $("#message-table").bootstrapTable({
        url: "/messageTable",
        method: "POST",
        sidePagination: "client",
        pagination: true,
        search: true,
        pageSize: 10,
        strictSearch: false,
        sortName: "time",
        sortOrder: 'desc',
        columns: [
            {
                title: 'Contact',
                field: 'username',
                align: 'center',
                valign: 'middle',
                width: '30%'
            },
            {
                title: 'Time',
                field: 'time',
                align: 'center',
                valign: 'middle',
                sortable: true,
                width: '70%',
                formatter: function (value, row, index) {
                    return '<a href="/messages?person=' + row['username'] + '">' + value + '</a>';
                }
            }
        ]
    });
})

$(document).ready(function () {
    $("#order-table").bootstrapTable({
        url: "/orderlist",
        method: "POST",
        sidePagination: "client",
        pagination: true,
        search: true,
        pageSize: 10,
        strictSearch: false,
        sortName: "time",
        sortOrder: "desc",
        columns: [
            {
                title: 'Type',
                field: 'type',
                align: 'center',
                valign: 'middle',
                width: '5%',
                formatter: function (value, row, index) {
                    if (value == 'selling') {
                        return '<span class="badge badge-pill badge-primary">selling</span>'
                    }
                    else if (value == 'buying') {
                        return '<span class="badge badge-pill badge-secondary">buying</span>'
                    }
                }
            },
            {
                title: 'Order Id',
                field: 'orderId',
                align: 'center',
                valign: 'middle',
                width: '15%',
                formatter: function (value, row, index) {
                    return '<a href="/OrderDetail?orderId=' + value + '">' + value + '</a>';
                }
            },
            {
                title: 'Product',
                field: 'product',
                align: 'center',
                valign: 'middle',
                width: '20%'
            },
            {
                title: 'Price',
                field: 'price',
                align: 'center',
                valign: 'middle',
                width: '20%'
            },
            {
                title: 'Status',
                field: 'status',
                align: 'center',
                valign: 'middle',
                width: '20%',
                sortable: true
            },
            {
                title: 'Time',
                field: 'time',
                align: 'center',
                valign: 'middle',
                width: '20%',
                sortable: true
            }
        ]
    });
})