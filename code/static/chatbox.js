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

    if (person === "") {
        alert("Please add contact person");
        return false;
    }

    addNewrReplies(message);

    mess = { "content": message, "receiverUsername": person }

    $.ajax({
        url: "newMessage",
        data: mess,
        type: 'POST',
        success: function (ret) {
            console.log("!!!")
            console.log(ret);
        }
    });

    return false;
}


// $('.submit').click(function (event) {
//     newMessage();
//     return false;
// });


$(document).ready(function () {
    Vue.component('listuser', {
        props: ['user'],
        template: '<li class="contact" v-on:click="userTop"><div class="wrap"><div class="meta"><p class="name"><i class="fas fa-user"style="margin-right:1vh"></i>{{user.username}}</p><p class="preview">{{user.time}}</p></div></div></li>',
        methods: {
            userTop: function () {
                this.$emit("move-top", this.user.username);
            }
        }
    });
    Vue.component('newuser', {
        props: [
            'errormessage'
        ],
        template: '<div id="user_modal" class="modal fade"><div class="modal-dialog"><div class="modal-content"><div class="modal-header"><h4 class="modal-title">Add new contact</h4><button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button></div><div class="modal-body"><form class="form-horizontal" role="form"><div class="form-group row"><label class="col-sm-4 col-form-label">User Name</label><div class="col-sm-6"><input type="text" class="form-control" id="sub_new_user" placeholder="User Name"></div></div><div class="form-group" style="color:red"' + 'v-if="errormessage">' + '{{errormessage}}</div></form></div><div class="modal-footer"><button type="button" class="btn btn-default" data-dismiss="modal">Close</button><button type="button" class="btn btn-primary" data-toggle="modal" v-on:click="createNewTalk">Create</button></div></div></div></div>',
        methods: {
            createNewTalk: function () {
                contactName = $('#sub_new_user').val();
                this.$emit("create-new-user", contactName);
            }
        }
    });
    var frame = new Vue({
        el: "#frame",
        data: {
            currentUser: '',
            currentTime: '0',
            chatMessage: [],
            users: [],
            addErrorMessage: null,
            tabList: ['info', 'buy', 'sell', 'order', 'message', 'favorite'],
            myname: '',
            system: {
                'username': "system",
                'time': ""
            },
            update: true,
        },
        created() {
            var self = this;
            var urlParams = new URLSearchParams(window.location.search);
            var startSection = urlParams.get("section");
            var startContact = urlParams.get("contact");

            this.myname = $('#myname').html();

            self.changeSection(startSection);
            $.ajax({
                url: 'messageTable',
                type: 'POST',
                dataType: 'json',
                success: function (data) {
                    self.$nextTick(function () {
                        let systemIndex = data.findIndex(function (x) { return x['username'] === 'system' });
                        if (systemIndex > -1) {
                            self.system.time = data[systemIndex]['time'];
                            self.currentTime = self.system.time;
                            self.currentUser = "system";
                            data.splice(systemIndex, 1)
                        }

                        self.users = data;
                        if (startContact === null || startContact === self.myname) {
                            self.loadMessge();
                        } else {
                            self.currentUser = startContact;
                            self.parentNewUser(startContact);
                        }
                    });

                    setTimeout(function () {
                        self.loadNewMessage();
                    }, 1000);

                }
            });

            $(window).on('keydown', function (e) {
                if (e.which == 13) {
                    newMessage(self.currentUser);
                    return false;
                }
            });
        },
        methods: {
            changeSection: function (section) {
                if (section === null) {
                    return;
                }
                $('#info').removeClass('active');
                $('#info-tab').removeClass('active');
                $('#info-tab').removeClass('in');
                $('#info-tab').addClass('fade');
                $('#' + section).addClass('active');
                $('#' + section + '-tab').removeClass('fade');
                $('#' + section + '-tab').addClass('in active');
            },
            loadNewMessage: function () {
                var person = this.currentUser;
                var time = this.currentTime;
                var self = this;

                if(!self.update){
                    return;
                }

                $.ajax({
                    url: 'messageTable',
                    type: 'POST',
                    dataType: 'json',
                    success: function (data) {
                        self.$nextTick(function () {
                            let systemIndex = data.findIndex(function (x) { return x['username'] === 'system' });
                            if (systemIndex > -1) {
                                self.system.time = data[systemIndex]['time'];
                                if (self.currentUser === 'system') {
                                    self.currentTime = self.system.time;
                                }
                                data.splice(systemIndex, 1);
                            }

                            self.users = data;
                        });
                    }
                });

                $.ajax({
                    url: 'getUpdateMessage',
                    type: 'POST',
                    dataType: 'json',
                    data: { "time": time, "receiver": person },
                    success: function (data) {
                        data.forEach(function (subMessage) {
                            if (subMessage["senderUsername"] === person) {
                                self.currentTime = subMessage['time'];
                                addNewSent(subMessage["content"]);
                            }
                        });

                        setTimeout(function () {
                            self.loadNewMessage();
                        }, 1000);
                    }
                });
            },
            loadMessge: function () {
                var person = this.currentUser;
                var self = this;
                self.update = false;

                $.ajax({
                    url: 'getAllMessage',
                    type: 'POST',
                    dataType: 'json',
                    data: { "receiver": person },
                    success: function (data) {
                        data.forEach(function (subMessage) {
                            self.currentTime = subMessage['time'];
                            if (subMessage["senderUsername"] === person) {
                                addNewSent(subMessage["content"]);
                            } else {
                                addNewrReplies(subMessage["content"]);
                            }
                        });
                        self.update = true;
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
                var myname = $('#myUserName').text();
                $.ajax({
                    url: 'userExist',
                    type: 'POST',
                    data: { "username": contactName },
                    success: function (data) {
                        if (data === 'success' && contactName !== myname) {
                            self.$nextTick(function () {
                                self.addErrorMessage = null;
                                if (!self.moveUserTop(contactName)) {
                                    self.currentUser = contactName;
                                    self.loadMessge();
                                }
                            });
                            $('#user_modal').modal('hide');
                        } else if (contactName === myname) {
                            self.$nextTick(function () {
                                self.addErrorMessage = "Please Add a New User";
                            });
                        } else {
                            self.$nextTick(function () {
                                self.addErrorMessage = "User Not Exists";
                            });
                        }
                    }
                });
            },
            moveUserTop: function (user) {
                emptyMessage();
                var self = this;
                self.$nextTick(() => {
                    self.currentUser = user;
                    self.loadMessge();
                });
            }
        }
    });
})