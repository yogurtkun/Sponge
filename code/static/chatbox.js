$(".messages").animate({ scrollTop: $(document).height() }, "fast");

function addNewrReplies(info) {
    $('<li class="replies"><p>' + info + '</p></li>').appendTo($('.messages ul'));
    $('.message-input input').val(null);
    $('.contact.active .preview').html('<span>You: </span>' + info);
    $(".messages").animate({ scrollTop: $(document).height() }, "fast");
}

function addNewSent(info) {
    $('<li class="sent"><p>' + info + '</p></li>').appendTo($('.messages ul'));
    $('.message-input input').val(null);
    $('.contact.active .preview').html('<span>You: </span>' + info);
    $(".messages").animate({ scrollTop: $(document).height() }, "fast");
}

function addNewUser(user, time) {
    $('<li class="contact"><div class="wrap"><div class="meta"><p class="name">' + user + '</p><p class="preview">' + time + '</p></div></div></li>').appendTo($('#contacts ul'));
}

function addPreUser(user) {
    $('<li class="contact"><div class="wrap"><div class="meta"><p class="name">' + user + '</p><p class="preview">' + '</p></div></div></li>').prependTo($('#contacts ul'));
}

function emptyUser() {
    $('#contacts ul').empty();
}

function emptyMessage() {
    $('.messages ul').empty();
}

function newMessage(person) {
    message = $(".message-input input").val();
    if ($.trim(message) == '') {
        return false;
    }

    addNewrReplies(message);

    mess = { "content": message, "receiverUsername": person }

    $.ajax({
        url: "newMessage",
        data: mess,
        type: 'POST',
        success: function (ret) {
            console.log(ret);
        }
    });

    return false;
}


// $('.submit').click(function (event) {
//     newMessage();
//     return false;
// });

$(window).on('keydown', function (e) {
    if (e.which == 13) {
        newMessage();
        return false;
    }
});


$(document).ready(function () {
    Vue.component('listuser', {
        props: ['user'],
        template: '<li class="contact" v-on:click="userTop"><div class="wrap"><div class="meta"><p class="name">{{user.username}}</p><p class="preview">{{user.time}}</p></div></div></li>',
        methods: {
            userTop: function () {
                this.$emit("move-top", this.user.username);
            }
        }
    });
    Vue.component('newuser', {
        template: '<div id="user_modal" class="modal fade"><div class="modal-dialog"><div class="modal-content"><div class="modal-header"><h4 class="modal-title">Add new contact</h4><button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button></div><div class="modal-body"><form class="form-horizontal" role="form"><div class="form-group row"><label class="col-sm-4 col-form-label">User Name</label><div class="col-sm-6"><input type="text" class="form-control" id="sub_new_user" placeholder="User Name"></div></div></form></div><div class="modal-footer"><button type="button" class="btn btn-default" data-dismiss="modal">Close</button><button type="button" class="btn btn-primary" data-toggle="modal" v-on:click="createNewTalk">Create</button></div></div></div></div>',
        methods: {
            createNewTalk: function () {
                contactName = $('#sub_new_user').val();
                this.$emit("create-new-user", contactName);
                $('#user_modal').modal('hide');
            }
        }
    });
    var frame = new Vue({
        el: "#frame",
        data: {
            currentUser: '',
            chatMessage: [],
            users: []
        },
        created() {
            var self = this;
            $.ajax({
                url: 'messageTable',
                type: 'POST',
                dataType: 'json',
                success: function (data) {
                    if (data.length == 0) {
                        return;
                    }
                    self.$nextTick(function () {
                        self.users = data;
                        self.currentUser = data[0]['username'];
                        self.loadMessge();
                    });
                }
            });
        },
        methods: {
            loadMessge: function () {
                var person = this.currentUser;
                $.ajax({
                    url: 'getAllMessage',
                    type: 'POST',
                    dataType: 'json',
                    data: { "receiver": person },
                    success: function (data) {
                        console.log(data)
                        data.forEach(function (subMessage) {
                            if (subMessage["senderUsername"] === person) {
                                addNewSent(subMessage["content"]);
                            } else {
                                addNewrReplies(subMessage["content"]);
                            }
                        })
                    }
                });
            },
            sendMessage: function () {
                newMessage(this.currentUser);
            },
            addNewContact: function () {
                $('#user_modal').modal('show');
            },
            parentNewUser: function (contactName) {
                var self = this;
                $.ajax({
                    url: 'userExist',
                    type: 'POST',
                    data: { "username": contactName },
                    success: function (data) {
                        if (data === 'success') {
                            self.$nextTick(function () {
                                if (!self.moveUserTop(contactName)) {
                                    self.users.unshift({
                                        'username': contactName,
                                        'time': null
                                    });
                                    self.currentUser = contactName;
                                    self.loadMessge();
                                }
                            });
                        }
                    }
                });
            },
            moveUserTop: function (user) {
                emptyMessage();
                var temp_user = null;
                var temp_index = -1;
                this.users.forEach(function (v, index) {
                    if (v['username'] == user) {
                        temp_user = v;
                        temp_index = index;
                    }
                });

                if (temp_index !== -1) {
                    var self = this;
                    this.$nextTick(function () {
                        self.users.splice(temp_index, 1);
                        self.users.unshift(temp_user);
                    })
                    self.currentUser = user;
                    self.loadMessge();
                    return true;
                } else {
                    return false;
                }
            }
        }
    });
})