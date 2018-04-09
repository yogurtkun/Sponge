var save = new Vue({
  el:"#post_info",
  data:{
  	title: undefined,
  	category: undefined,
  	location: undefined,
  	postId: undefined,
  	postType: undefined,
  	price: undefined,
  	sellerName: undefined,
  	description: undefined,
    imageName:"Select file...",

    is_update_success:undefined,
  },
  mounted(){
  	this.query_post_info()
  },
  methods:{
  	query_post_info(){
  		this.set_postType_postId()

  		tdata={"postType":this.postType, "postId":this.postId}

	    $.ajax({
	    url: '/getPostData',
	    dataType: 'json',
        type: "POST",
	    data: tdata,

	    success: (json)=>{
	      console.log(json);
	      this.title = json.title
	      this.category = json.category
	      this.location = json.location
	      this.price = json.price
	      this.sellerName = json.sellerName
	      this.description = json.description
	    },
	    }).fail(function($xhr) {
	      var data = $xhr.responseJSON;
	      console.log(data);
	    });
	  },

    set_postType_postId(){
	    var href = window.location.href;
        var postType = href.substring(href.indexOf("postType")+9, href.indexOf("&"))
        var postId = href.substr(href.indexOf("postId")+7, 9)

        this.postType = postType
        this.postId = postId
	},

  	save_post: function(){

  		if(this.title.length == 0 || this.description.length == 0){
  			this.is_update_success = false
  			return
  		}

  		tdata={"postType":this.postType, "postId":this.postId,
  				"title": this.title, "category": this.category,
  				"location": this.location, "price": this.price,
  				"description": this.description,
  				"image":this.imageName}

	    $.ajax({
	    url: '/updatepost',
	    dataType: 'json',
        type: "POST",
	    data: tdata,

	    success: (json)=>{
	      console.log(json);
		  this.is_update_success = true
		  
	      console.log(this.postType);
		  if (this.postType === 'Seller') {
			window.location = '/SellerPost\?postId=' + this.postId
		  }
		  if (this.postType === 'Buyer') {
			window.location = '/BuyerPost\?postId=' + this.postId
		  }
	    },
	    }).fail(function($xhr) {
	      var data = $xhr.responseJSON;
	      console.log(data);
	      this.is_update_success = false
	    });
    },

    updateFile: function(event){
      let imageinput =  $('#InputImage').prop('files')

      if(imageinput.length !== 0)
        this.imageName = imageinput[0].name;
    }
  },
});

function isNormalInteger(str) {
    var n = Math.floor(Number(str));
    return n !== Infinity && String(n) === str && n >= 0;
}

(function () {
    'use strict';
    window.addEventListener('load', function () {
        // Fetch all the forms we want to apply custom Bootstrap validation styles to
        var forms = document.getElementsByClassName('needs-validation');
        // Loop over them and prevent submission
        var validation = Array.prototype.filter.call(forms, function (form) {
            form.addEventListener('submit', function (event) {
                let imageinput =  $('#InputImage').prop('files')

                if(imageinput.length !== 0 && imageinput[0].size >= 51200){
                    alert("Image too large");
                    event.preventDefault();
                    event.stopPropagation();
                }

                if (imageinput.length !== 0 &&imageinput[0].type !== 'image/jpeg' && imageinput[0].type !== 'image/png' && imageinput[0].type !== 'image/gif') {
                    alert('The type of file is incorrect!');
                    event.preventDefault();
                    event.stopPropagation();
                }

                let price = $('input[name=price]')[0].value;
                if( !isNormalInteger(price) && price !== ""){
                    alert("Price incorrect");
                    event.preventDefault();
                    event.stopPropagation();
                }

                if (form.checkValidity() === false) {
                    event.preventDefault();
                    event.stopPropagation();
                }

                form.classList.add('was-validated');
            }, false);
        });
    }, false);
})();