$(document).ready(() => {
    var userinfo = new Vue({
        el: '#user-info',
        data: {
            user: { 'username': "Empty", "email": "Empty", "zipcode": "Empty", "phonenumber": "Empty", "address": "Empty" }
        },
        methods: {
            changeInfo: function(){
                $.ajax({
                    url: '/updateUser',
                    type: 'POST',
                    data: this.user,
                    success: (data)=>{
                        if(data === "Success"){
                            alert("Save Successfully");
                        }else{
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
                    this.user = Object.assign({},retUser);

                    for(let k in this.user){
                        if(this.user[k] === "" || this.user[k] === null ){
                            this.user[k] = "";
                        }
                    }
                }
            });
        }
    });
});