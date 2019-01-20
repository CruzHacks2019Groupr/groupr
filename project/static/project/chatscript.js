//initiate puhser with your application key
var pusher = new Pusher('4105ec1d8d985dcf27bf', {
    cluster: 'us2'
});
//subscribe to the channel you want to listen to
var my_channel = pusher.subscribe({{ room }});
//wait for an event to be triggered in that channel
my_channel.bind("an_event", function (data) {
    // declare a variable new_message to hold the new chat messages
    var new_message = `<li class="left clearfix"><span class="chat-img pull-left">
                        <img src="http://placehold.it/50/55C1E7/fff&text=`+data.name+`" alt="User Avatar" class="img-circle">
                    </span>
                        <div class="chat-body clearfix">
                            <div class="header">
                                <strong class="primary-font">`+data.name+`</strong> <small class="pull-right text-muted">
                            </div>
                            <p>
                               `+data.message+`
                            </p>
                        </div>
                    </li>`;
    //append the new message to the ul holding the chat messages
    $('#chat').append(new_message);
});
//wait until the DOM is fully ready
$(document).ready(function(){
//add event listener to the chat button click 
    $("#btn-chat").click(function(){
//get the currently typed message
         var message = $('#btn-input').val();

        $.post({
            url: '/ajax/chat/',
            data: {
            'message': message
            },
            success: function (data) {

                $('#btn-input').val('');

            }
        });

    })
    })