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

$(document).ready(function(){
    $("#message-table").bootstrapTable({
        url:"/messageTable",
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
                    return '<a href="/messages?person='+row['username']+'">'+value+'</a>';
                }
            }
        ]
    });
})