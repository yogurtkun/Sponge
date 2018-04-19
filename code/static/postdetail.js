
Vue.use(bootstrapVue);
var checkVue = new Vue({
    el: "#checkbutton",
    methods: {
        checkout: function () {
            var urlParams = new URLSearchParams(window.location.search);
            var postId = urlParams.get("postId");
            window.location.href = "/buyorder?postId=" + postId;
        }
    }
});


var favoriteBtn = new Vue({
    el: "#favoriteBtn",
    data: {
        post_item: undefined,
        is_favorite: undefined,
        postType: undefined,
        postId: undefined,
        color_favorite: '#f10215',
        color_not_favorite: 'black',
    },
    mounted() {
        var href = window.location.href;
        var pathname = window.location.pathname;
        var post_type = pathname.substring(1, pathname.length)
        var postid = href.substring(href.indexOf("postId") + 7, href.length)

        this.postId = postid
        if (post_type === "SellerPost") {
            this.postType = "Seller"
        }
        else if (post_type === "BuyerPost") {
            this.postType = "Buyer"
        }



        if (post_type === "SellerPost") {
            $.ajax({
                url: '/postlist/seller',
                dataType: 'json',
                type: "POST",

                success: (json) => {
                    this.post_item = json;
                    if (this.post_item !== undefined) {
                        for (var i = 0; i < this.post_item.length; i++) {
                            if (this.post_item[i].postId === parseInt(postid)) {
                                this.post_item = this.post_item[i]
                                this.is_favorite = this.post_item.favorite
                            }
                        }
                    }
                },
            }).fail(function ($xhr) {
                var data = $xhr.responseJSON;
                console.log(data);
            });
        }
        else if (post_type === "BuyerPost") {
            $.ajax({
                url: '/postlist/buyer',
                dataType: 'json',
                type: "POST",

                success: (json) => {
                    this.post_item = json;
                    if (this.post_item !== undefined) {
                        for (var i = 0; i < this.post_item.length; i++) {
                            if (this.post_item[i].postId === parseInt(postid)) {
                                this.post_item = this.post_item[i]
                                this.is_favorite = this.post_item.favorite
                            }
                        }
                    }
                },
            }).fail(function ($xhr) {
                var data = $xhr.responseJSON;
                console.log(data);
            });
        }
    },
    methods: {
        favorite_decider: function () {
            if (this.is_favorite === false) {
                this.addFavorite(this.postType, this.postId)
            }
            else {
                this.deleteFavorite(this.postType, this.postId)
            }
        },

        deleteFavorite: function (postType, postId) {
            this.is_favorite = false

            tdata = { "postType": postType, 'postId': postId }
            $.ajax({
                url: '/deleteFavorite',
                type: 'POST',
                data: tdata,
                success: (data) => {
                    console.log("success!")
                }
            })
        },

        addFavorite: function (postType, postId) {
            this.is_favorite = true

            tdata = { "postType": postType, 'postId': postId }
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
    methods: {
        delete_post: function (postType, postId) {
            console.log("delete_post")

            tdata = { "postType": postType, 'postId': postId }
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

var urlParams = new URLSearchParams(window.location.search);
var postId = urlParams.get("postId");
var postType = "";
if (window.location.href.includes("Seller")) {
    postType = "Seller";
} else {
    postType = "Buyer";
}

var comment_info = new Vue({
    el: "#comment-tab",
    data: {
        newComment: "",
        messages: [],
        sendTo: null,
        sessionUser:$('#sessionUser').html(),
        deleteId: null,
        text_max: 300,
        text_length: 0
    },
    watch:{
        newComment: function(){
            this.text_length = this.newComment.length;
        }
    },
    created() {
        var self = this;
        $.ajax({
            url: 'getPostComments',
            type: 'POST',
            dataType: 'json',
            data: { "postType": postType, "postId": postId },
            success: function (data) {
                self.messages = data;
                console.log(data);
            }
        })
    },
    methods: {
        sendComment: function () {
            if(this.newComment === ""){
                $('textarea').attr("placeholder","Please Input Comment!");
                return;
            }

            data = {
                "postType":postType,
                "postId" : postId,
                "content": this.newComment
            };
            if(this.sendTo !== null){
                data['replyTo'] = this.sendTo;
            }

            $.ajax({
                url:'addPostComment',
                type:'POST',
                dataType: 'json',
                data: data,
                success: function(data){
                    if(data.indexOf("succeeded") >=0 ){
                        $("#success_comment").modal('show');
                        setTimeout(function(){ window.location.reload(false)},500);
                    }else{
                        alert("Add Comment failed");
                    }
                }
            })
            this.sendTo = null;
        },
        replyParent: function(replyUser){
            this.sendTo = replyUser;
            $('textarea').attr("placeholder","Reply to "+replyUser);
        },
        deleteParent: function(commentId){
            $("#delete_comment").modal('show');
            this.deleteId = commentId;
        },
        deleteConfirm: function(){
            var self = this;
            $.ajax({
                url:"delPostComment",
                type:"POST",
                dataType: 'json',
                data: {'postType':postType,'commentId':self.deleteId},
                success: function(data){
                    if(data === "del comment failed" ){
                        alert("Delete failed");
                    }else{
                        window.location.reload(false);
                    }
                }
            });
        }

    }
});

Vue.component('comment', {
    props: [
        'message',
        'i',
        'am',
        'cu'
    ],
    template: `
        <div class="comment-card card-body">
            <div class="mt-0 comment-div">
                <a :href="'/UserInfo?username='+message.author">{{message.author}}</a>
                <span v-if="message.replyTo!==null" class="comment-span">reply to </span>
                <a v-if="message.replyTo!==null" :href="'/UserInfo?username='+message.replyTo">{{message.replyTo}}</a>
                <div  style="float: right;max-height:25px">
                <span class="comment-span">{{message.time}}</span>
                <button v-on:click="reply" class="btn">
                <i class="fas fa-reply"></i>
                </button>
                <button v-if="message.author===cu" v-on:click="deleteM" class="btn">
                <i class="far fa-trash-alt"></i>
                </button>
                </div>
            </div>
            <p style="margin-top: 0.5vh">{{message.content}}</p>
            <hr v-if="i !== am.length-1" class="comment-hr">
        </div>
    `,
    methods: {
        reply: function(){
            this.$emit("reply-message",this.message['author']);
            $('html, body').animate({
                scrollTop: $("textarea").offset().top
            }, 200);
            $("textarea").focus();
        },
        deleteM: function(){
            this.$emit("delete-message",this.message['commentId'])
        }
    }
});
