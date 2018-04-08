
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
  post_item : undefined,
  is_favorite : undefined,
  postType: undefined,
  postId:undefined,
  color_favorite: '#f10215',
  color_not_favorite: 'black',
},
mounted(){
  var href = window.location.href;
  var pathname = window.location.pathname;
  var post_type = pathname.substring( 1, pathname.length)
  var postid = href.substring(href.indexOf("postId") + 7, href.length)

  this.postId = postid
  if(post_type === "SellerPost")
  {
      this.postType = "Seller"
  }
  else if(post_type ==="BuyerPost")
  {
      this.postType = "Buyer"
  }



  if(post_type === "SellerPost")
  {
    $.ajax({
        url: '/postlist/seller',
        dataType: 'json',
        type: "POST",

        success: (json)=>{
            this.post_item = json;
            if(this.post_item !== undefined)
            {
              for(var i = 0; i < this.post_item.length; i++)
              {
                if(this.post_item[i].postId === parseInt(postid))
                {
                  this.post_item = this.post_item[i]
                  this.is_favorite = this.post_item.favorite
                }
              }
            }
        },
        }).fail(function($xhr) {
            var data = $xhr.responseJSON;
            console.log(data);
    });
  }
  else if(post_type === "BuyerPost")
  {
    $.ajax({
        url: '/postlist/buyer',
        dataType: 'json',
        type: "POST",

        success: (json)=>{
          this.post_item = json;
          if(this.post_item !== undefined)
          {
            for(var i = 0; i < this.post_item.length; i++)
            {
              if(this.post_item[i].postId === parseInt(postid))
              {
                this.post_item = this.post_item[i]
                this.is_favorite = this.post_item.favorite
              }
            }
          }
        },
        }).fail(function($xhr) {
            var data = $xhr.responseJSON;
            console.log(data);
    });
  }
},
methods:{
  favorite_decider: function(){
      if(this.is_favorite === false)
      {
          this.addFavorite(this.postType, this.postId)
      }
      else
      { 
          this.deleteFavorite(this.postType, this.postId)
      }
  },

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