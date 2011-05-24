$(document).ready(function() {
    $.getJSON('/autofill', function(data) {
        $(".crush").autocomplete({
            minLength: 1,
            delay: 0,
            source: data,
            select: function(event, ui) {
                $(this).val("");
                    $.post("/crushes/add", { "crush": ui.item.carletonID }, function(data) {
                        if (data.success == 0) {
                            if ($('#crush-' + ui.item.carletonID).length == 0) {
                                var status;
                                if (data.status == "not_paired") { status = '<span style="color:red;">not yet registered</span><br>'; }
                                else if (data.status == "opted_out") { status = '<span style="color:red;">opted out</span><br>'; }
                                else { status = '<span style="color:green;">participating!</span><br>'; }
                                $("#crushes").append('<div id="crush-' + ui.item.carletonID + '" class="crushdiv"><img src="/user_images/' + ui.item.carletonID + '.jpg" width="120" height="120"><br>' + ui.item.first_name + " " + ui.item.last_name + "<br>" + status + '<button class="messageCrush" value="' + ui.item.carletonID + '" data-first-name="' + ui.item.first_name + '" data-last-name="' + ui.item.last_name + '">message</button> <button class="removeCrush" value="' + ui.item.carletonID + '">remove</button></div>');
                            }
                        }
                        else if (data.success == 1) { alert("Your account must be paired and opted-in in order to add crushes. Go to the settings page to resolve this issue."); }
                        else if (data.success == 2) { alert(ui.item.first_name + " " + ui.item.last_name + " is already one of your crushes."); }
                        else if (data.success == 3) { alert(ui.item.first_name + " " + ui.item.last_name + " is not in our database."); }
                        else if (data.success == 4) { alert("You cannot choose yourself as a crush."); }
                        else if (data.success == 5) { alert("Sorry. You can't have more than 5 crushes. Please remove one before adding another."); }
                        else { alert("There was an error in adding your crush. Please try again."); }
                    }, "json");
                return false; // tells autocomplete not to update the field with the selected value
            }
        });
    });

    $("#new-message-form").dialog({
        autoOpen: false,
        height: 400,
        width: 450,
        modal: true,
        buttons: {
            "Send Message": function() {
                                var to = $("input[name='message-to']").val();
                                var name = $("input[name='message-to-box']").val();
                                var body = $("textarea[name='message-body']").val();
                                if (body == "") { alert("Please enter a message body."); return; }
                                $.post("/messages/send", { "to": to, "body": body }, function(data) {
                                    if (data.success == 0) {
                                        $("#new-message-form").dialog("close");
                                        $(".message-item").removeClass("just-sent");
                                        addSentMessage(data.name, body, data.mid);
                                        showMessages('from-me');
                                    }
                                    else if (data.success == 1) { alert("Your account must be paired and opted-in in order to send messages."); }
                                    else if (data.success == 2) { alert(name + " is not in our database. Could not send message."); }
                                    else if (data.success == 3) { alert(name + " is not one of your crushes. You can only send a message to one of your crushes. Refresh the page to get the most updated list of your crushes."); }
                                    else if (data.success == 4) { alert("Your message did not have a body. It was not sent."); }
                                    else { alert("There was an error in sending your message. Please try again."); }
                                }, "json");
                            },
            Cancel: function() { $(this).dialog("close"); }
        },
        close: function() { $("textarea[name='message-body']").val(""); }
    });
    
    $(".messageCrush:button").live('click', messageSendListener);
    $(".removeCrush:button").live('click', crushRemoveListener);
    $(".reply-button").live('click', messageReplyListener);
    $(".delete-button").live('click', messageRemoveListener);
    $(".block-button").live('click', blockUserListener);
    $(".reply-text").live('keyup', messageSendReplyListener);
});

function addSentMessage(to, body, message_id) {
    var message =
    $('<div class="message" data-mid="' + message_id + '">' +
    '  <div class="message-item unread sent">' +
    '    <div class="message-item-header">' +
    '    <div class="message-item-info"><strong>You</strong> to <strong>' + to + '</strong> just now</div>' +
    '    <div class="message-actions">' +
    '      <ul class="icons ui-widget ui-helper-clearfix">' +
    '        <li class="ui-state-default ui-corner-all reply-button" title="Reply"><span class="ui-icon ui-icon-arrowreturnthick-1-w"></span></li>' +
    '        <li class="ui-state-default ui-corner-all delete-button" title="Delete"><span class="ui-icon ui-icon-trash"></span></li>' +
    '        <li class="ui-state-default ui-corner-all block-button" title="Block User"><span class="ui-icon ui-icon-cancel"></span></li>' +
    '      </ul>' +
    '    </div>' +
    '    </div>' +
	'    <div class="message-item-body">' + body + '</div>' +
	'  </div>' +
	'  <div class="message-item reply reply-box" style="display:none;"><input type="text" class="reply-text"></div>' +
	'</div>');
	if ($("#messages-from-me .messages .message").length > 0) { $("#messages-from-me .messages .message:first").before(message); }
	else { $("#messages-from-me .messages").html(message); }
	message.find(".message-item").each(function() { $(this).removeClass('unread', 3000); });
}

function crushRemoveListener() {
    var crush = $(this);
    crush.parent().fadeOut("fast");
    $.post("/crushes/remove", { "crush": crush.val() }, function(data) {
        if (data.success == 0) { crush.parent().remove(); }
        else if (data.success == 1) { alert("Your account must be paired and opted-in in order to remove crushes. Go to the settings page to resolve this issue."); crush.parent().show(); }
        else if (data.success == 2) { alert("The username " + crush.val() + " does not exist and thus could not be removed. It might have been already removed."); crush.parent().remove(); }
        else { alert("Error in deleting crush. Try again."); crush.parent().show(); }
    }, "json");
}

function messageSendListener(user) {
    $("#new-message-form input[name='message-to']").val($(this).val());
    $("#new-message-form input[name='message-to-box']").val($(this).attr("data-first-name") + ' ' + $(this).attr("data-last-name")); // make this their first name and last name
    $("#new-message-form").dialog("open");
}

function messageRemoveListener() {
    if (confirm("Do you really want to delete this message?")) {
        var message = $(this).parent().parent().parent().parent().parent();
        message.fadeOut("fast");
        $.post("/messages/delete", { "mid": message.attr("data-mid") }, function(data) {
            if (data.success == 0) { message.remove(); }
            else if (data.success == 1) { alert("Your account must be paired and opted-in in order to delete messages. Go to the settings page to resolve this issue."); message.show(); }
            else if (data.success == 2) { alert("Message does not exist or you tried to delete another user's message."); message.remove(); }
            else { alert("Error in deleting message. Try again."); message.show(); }
        }, "json");
    }
}

function showMessages(tab) {
    $(".messages-tab").hide();
    $("#messages-" + tab).show();
    $("#messages-nav li").removeClass("active");
    $("#messages-nav-" + tab).addClass("active");
}

function messageReplyListener() {
    $(this).parent().parent().parent().parent().next(".reply-box").show();
    $(this).parent().parent().parent().parent().next(".reply-box").find("input").focus(); // bug here that causes hitting enter to send many replies
}

function messageSendReplyListener(event) {
    if (event.keyCode == 13) {
      var message_id = $(this).parent().parent().attr("data-mid");
      var body = $(this).val();
      $(this).val("");
      $(this).parent().before('<div class="message-item sent reply"><div class="message-item-header"><div class="message-item-info"><strong>You</strong> just now</div></div><div class="message-item-body">' + body + '</div></div>');
      $.post("/messages/reply", { "mid": message_id, "body": body }, function(data) {
        if (data.success == 0) { }
        else if (data.success == 1) { alert("Your account must be paired and opted-in in order to reply to messages. The added message will be gone when you refresh the page. Go to the settings page to resolve this issue."); }
        else if (data.success == 2) { alert("Message does not exist or you tried to reply another user's message. The added message will be gone when you refresh the page."); }
        else { alert("Error in replying to  message. Try again. The added message will be gone when you refresh the page."); }
      }, "json");
    }
}

function blockUserListener() {
    alert("feature not implemented yet. sorry");
}