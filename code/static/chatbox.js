function getMessageHeight(){
    var h = 0;
    for(p of $('.sent')){
        h += (p.offsetHeight+5);
    }
    for(p of $('.replies')){
        h += (p.offsetHeight+5);
    }
    return h;
}

var TIME_TO_FETCH_MESSAGE = 1000;
$(".messages").animate({ scrollTop: getMessageHeight() }, "fast");

function addNewrReplies(info) {
    $('<li class="replies"><p>' + info + '</p></li>').appendTo($('.messages ul'));
    $('.message-input input').val(null);
    $('.contact.active .preview').html('<span>You: </span>' + info);
}

function addNewSent(info) {
    $('<li class="sent"><p>' + info + '</p></li>').appendTo($('.messages ul'));
    $('.message-input input').val(null);
    $('.contact.active .preview').html('<span>You: </span>' + info);
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
        template: '<li class="contact" v-on:click="userTop"><div class="wrap"><div class="meta"><p class="name"><i class="fas fa-user"style="margin-right:1vh"></i>{{user.username}}<div v-if="user.unseen !== 0" class="numberCircle">{{user.unseen}}</div></p><p class="preview">{{user.time}}</p></div></div></li>',
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
                'time': "",
                'unseen':0,
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
                            self.system.unseen = data[systemIndex]['unseen']
                            // self.currentTime = self.system.time;
                            // self.currentUser = "system";
                            data.splice(systemIndex, 1)
                        }

                        self.users = data;
                        if (startContact === null || startContact === self.myname) {
                            self.loadMessge();
                        } else {
                            self.parentNewUser(startContact);
                        }
                    });

                    setTimeout(function () {
                        self.loadNewMessage();
                    }, TIME_TO_FETCH_MESSAGE);

                }
            });

            $(window).on('keydown', function (e) {
                if (e.which == 13) {
                    newMessage(self.currentUser);

                    $(".messages").animate({ scrollTop: getMessageHeight() }, "fast");
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

                if (!self.update) {
                    setTimeout(function () {
                        self.loadNewMessage();
                    }, 1000);
                    return;
                }

                self.update = false;

                $.ajax({
                    url: 'messageTable',
                    type: 'POST',
                    dataType: 'json',
                    success: function (data) {
                        self.$nextTick(function () {
                            let systemIndex = data.findIndex(function (x) { return x['username'] === 'system' });
                            if (systemIndex > -1) {
                                self.system.time = data[systemIndex]['time'];
                                self.system.unseen = data[systemIndex]['unseen'];
                                if (self.currentUser === 'system') {
                                    self.currentTime = self.system.time;
                                }
                                data.splice(systemIndex, 1);
                            }

                            self.users = data;
                            self.update = true;
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
                        $(".messages").animate({ scrollTop: getMessageHeight() }, "fast");
                        self.update = true;
                    }
                });
            },
            sendMessage: function () {
                newMessage(this.currentUser);

                $(".messages").animate({ scrollTop: getMessageHeight() }, "fast");
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

                var el = document.querySelector('#notification');

                (function () {
                    var update = function (count) {
                        if (el == null) {
                            return;
                        }
                        el.setAttribute('data-count', count);
                        el.classList.remove('notify');
                        el.offsetWidth = el.offsetWidth;
                        el.classList.add('notify');
                        if (count === 0) {
                            el.classList.remove('show-count');
                        } else {
                            el.classList.add('show-count')
                        }
                    }

                    // get new message count
                    $.ajax({
                        url: '/countUnreadMessage',
                        type: 'POST',
                        success: (data) => {
                            update(parseInt(data))
                        },
                    }).fail(function ($xhr) {
                        var data = $xhr.responseJSON;
                    });


                })();
            }
        }
    });
})