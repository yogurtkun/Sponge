Vue.component('postitems', {
  props: 
  {
    postid:
    {
      type: String,
      required: true
    },
    title: 
    {
      type: String,
      required: true
    },
    category:
    {
      type: String,
      required: true
    },
    description: 
    {
      type: String,
      required: true
    },
    price: 
    {
      type: Number,
    },
    time: 
    {
      type: String,
      required: true
    },
    like: 
    {
      type: Boolean,
      required: true
    },
    user:
    {
      type: String,
      required: true
    },
    location:
    {
      type: String,
      required: true
    },
    imageDir:
    {
      type: String,
    }
  },
  //template: '<div>{{ postid }}{{ title }}{{ description }}{{ price }}{{ time }}{{ like }}</div>'
  //template: '<div class="card container-fluid"><img  src="static/test.jpg" alt="image" height="100" width="100"><div class="card-body"><h5 class="card-title">Item:{{title}}</h5><p class="card-text">Description:{{description}}</p><p class="card-text">Category:{{category}}</p><p class="card-text">Location:{{location}}</p><p class="card-text">Poster:{{user}}</p><p class="card-text">Price:{{price}}</p><p class="card-text">{{time}}</p><p class="card-text">Like:{{like}}</p><a v-bind:href="postid" class="btn btn-primary">Detail</a></div></div>'
  template: '<div class="card container-fluid"><img src="static/test.jpg" alt="image" height="100" width="100"><div class="card-body"><h5 class="card-title">Item:{{title}}</h5><p class="card-text">Description:{{description}}</p><p class="card-text">Category:{{category}}</p><p class="card-text">Location:{{location}}</p><p class="card-text">Poster:{{user}}</p><p class="card-text">Price:{{price}}</p><p class="card-text">{{time}}</p><p class="card-text">Like:{{like}}</p><a v-bind:href="postid" class="btn btn-primary">Detail</a></div></div>'
});

Vue.component('category', {
  props: 
  {
    category:
    {
      type: String,
      required: true
    },
  },
  template: '<a v-bind:href="category">{{category}}</a>'
});

var items = new Vue({
  el: '#postitem',
  data: {
    items: [
    {"postid": "1111", "category": "ca1", "title": "1", "description": "2", "price": 3, "time": "2018-03-15", "like": true, "user":"user123", "location":"NY", "imageDir":"static/test.jpg"},
    {"postid": "2222", "category": "ca1", "title": "1", "description": "2", "price": 3, "time": "2018-03-15", "like": true, "user":"user123", "location":"NY", "imageDir":"static/test.jpg"},
    {"postid": "3333", "category": "ca1", "title": "1", "description": "2", "price": 3, "time": "2018-03-15", "like": true, "user":"user123", "location":"NY", "imageDir":"static/test.jpg"},
    ]
  },
  created(){
    $.ajax({
      url: '/testPostList',
      dataType: 'json',
      type: "POST",

      success: (json)=>{
          console.log(json);
          this.items = json.data;
      },
      }).fail(function($xhr) {
          var data = $xhr.responseJSON;
          console.log(data);
      });
  },
});

var category = new Vue({
  el: '#category',
  data: {
    category: [
    {"category": "ca1"},
    {"category": "ca2"},
    {"category": "ca3"},
    ]
  },
  created(){
    $.ajax({
      url: '/testCategory',
      dataType: 'json',
      type: "POST",

      success: (json)=>{
          console.log(json);
          this.category = json.data;
      },
      }).fail(function($xhr) {
          var data = $xhr.responseJSON;
          console.log(data);
      });
  },
});
