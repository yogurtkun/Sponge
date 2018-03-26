$(".messages").animate({ scrollTop: $(document).height() }, "fast");

var person;

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

function newMessage() {
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
    var frame = new Vue({
        el: "#frame",
        data: {
            talkers: [],
            chatMessage: []
        },
        created() {
            var self = this;
            var urlParams = new URLSearchParams(window.location.search);
            person = urlParams.get("person");
            $.ajax({
                url: 'messageTable',
                type: 'POST',
                dataType: 'json',
                success: function (data) {
                    var temp_talkers = [person];
                    for (it of data) {
                        if (it.username !== person) {
                            temp_talkers.push(it.username);
                        }
                    }
                    self.$nextTick(function () {
                        self.talkers = temp_talkers;
                    })
                }
            });
            $.ajax({
                url: 'getAllMessage',
                type: 'POST',
                dataType: 'json',
                data: { "receiver": person },
                success: function (data) {
                    console.log(data)
                    data.forEach(function(subMessage){
                        if(subMessage["senderUsername"] === person){
                            addNewSent(subMessage["content"]);
                        }else{
                            addNewrReplies(subMessage["content"]);
                        }
                    })
                }
            });
        },
        methods: {
            sendMessage: function () {
                newMessage();
            }
        }
    });
})