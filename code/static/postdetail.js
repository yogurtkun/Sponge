$("#favoriteBtn").attr('class', 'visible');


Vue.use(bootstrapVue);
var checkVue = new Vue({
  el:"#checkbutton",
  methods: {
    checkout: function(){
      var urlParams = new URLSearchParams(window.location.search);
      var postId = urlParams.get("postId");
      window.location.href = "/buyorder?postId="+postId;
    }
  }
});


var favoriteBtn = new Vue({
el: "#favoriteBtn",
data: {
  is_favorite : undefined
},
methods:{
  deleteFavorite : function(postType, postId){
    this.is_favorite = false

    tdata = {"postType": postType, 'postId': postId}
    $.ajax({
        url: '/deleteFavorite',
        type: 'POST',
        data: tdata,
        success: (data) => {
            console.log("success!")
        }
    })
  },

  addFavorite : function(postType, postId){
    this.is_favorite = true

    tdata = {"postType": postType, 'postId': postId}
    console.log("add", tdata);
    $.ajax({
        url: '/favorite',
        type: 'POST',
        data: tdata,
        success: (data) => {
            console.log("success!")
        }
      })
    } 
  }
});

var showmore = new Vue({
    el: "#more-button",
    data: {

    },
    methods:{
        edit_post: function(postType, postId){
            console.log("edit_post")
            tdata = {"postType": postType, 'postId': postId}
            $.ajax({
                url: '/editpost',
                type: 'POST',
                data: tdata,
                success: (data) => {
                    console.log("success!")
                }
              }) 
        },
    },
});

var delete_post = new Vue({
    el: "#delete_window",
    data: {

    },
    methods:{
        delete_post: function(postType, postId){
            console.log("delete_post")
            
            tdata = {"postType": postType, 'postId': postId}
            $.ajax({
                url: '/deletepost',
                type: 'POST',
                data: tdata,
                success: (data) => {
                    console.log("success!")
                    if (postType === 'Seller') {
                        window.location = '/portal?section=sell'
                    }
                    if (postType === 'Buyer') {
                        window.location = '/portal?section=buy'
                    }
                }
            })
        },
    },
});