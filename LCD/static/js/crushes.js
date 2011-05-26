$(document).ready(function() {
    
    var tab = readCookie("tabSelection");
    if (tab) { showMessages(tab); }
    updateMessages();
    
    checkNoMessages();
    checkNoCrushes();

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
                        else if (data.success == 1) { alert("Your account must be paired and opted-in in order to add crushes. Redirecting to settings page to resolve the issue..."); window.location='/settings'; }
                        else if (data.success == 2) { alert(ui.item.first_name + " " + ui.item.last_name + " is already one of your crushes."); }
                        else if (data.success == 3) { alert(ui.item.first_name + " " + ui.item.last_name + " is not in our database."); }
                        else if (data.success == 4) { alert("You cannot choose yourself as a crush."); }
                        else if (data.success == 5) { alert("Sorry. You can't have more than 5 crushes. Please remove one before adding another."); }
			else if (data.success == 6) { alert("Sorry. Last Chance Dance has closed and you are not allowed to add crushes anymore. Redirecting..."); window.location='/'; }
                        else { alert("There was an error in adding your crush. Please try again."); }
			checkNoCrushes();
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
        resizable: false,
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
                                        checkNoMessages();
                                        showMessages('from-me');
                                    }
                                    else if (data.success == 1) { alert("Your account must be paired and opted-in in order to send messages. Redirecting to settings page to resolve the issue..."); window.location='/settings'; }
                                    else if (data.success == 2) { alert(name + " is not in our database. Could not send message."); }
                                    else if (data.success == 3) { alert(name + " is not one of your crushes. You can only send a message to one of your crushes. Refresh the page to get the most updated list of your crushes."); }
                                    else if (data.success == 4) { alert("Your message did not have a body. It was not sent."); }
				    else if (data.success == 6) { alert("Sorry. Last Chance Dance has closed and you are not allowed to send messages anymore. Redirecting..."); window.location='/'; }
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
    $(".delete-button").live('click', messageDeleteListener);
    $(".report-abuse-button").live('click', reportUserListener);
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
    '        <li class="ui-state-default ui-corner-all report-abuse-button" title="Report Abuse"><span class="ui-icon ui-icon-alert"></span></li>' +
    '      </ul>' +
    '    </div>' +
    '    </div>' +
	'    <div class="message-item-body">' + body + '</div>' +
	'  </div>' +
	'  <div class="message-item reply reply-box" style="display:none;"><input type="text" class="reply-text"></div>' +
	'</div>');
	if ($("#messages-from-me .messages .message").length > 0) { $("#messages-from-me .messages .message:first").before(message); }
	else { $("#messages-from-me .messages").html(message); }
	message.find(".message-item").each(function() { $(this).removeClass('unread', 500); }); // small bug here that closes reply box if you open before class removed
}

function crushRemoveListener() {
    var crush = $(this);
    if (confirm("Do you really want to remove this person from your list of crushes?")) {
        crush.parent().fadeOut("fast");
        $.post("/crushes/remove", { "crush": crush.val() }, function(data) {
            if (data.success == 0) { crush.parent().remove(); }
            else if (data.success == 1) { alert("Your account must be paired and opted-in in order to remove crushes. Redirecting to settings page to resolve the issue..."); window.location='/settings'; }
            else if (data.success == 2) { crush.parent().remove(); alert("The username " + crush.val() + " does not exist and thus could not be removed. It might have been already removed."); }
	    else if (data.success == 6) { alert("Sorry. Last Chance Dance has closed and you are not allowed to modify crushes anymore. Redirecting..."); window.location='/'; }
            else { alert("Error in deleting crush. Try again."); crush.parent().show(); }
	    checkNoCrushes();
        }, "json");
    }
}

function messageSendListener(user) {
    $("#new-message-form input[name='message-to']").val($(this).val());
    $("#new-message-form input[name='message-to-box']").val($(this).attr("data-first-name") + ' ' + $(this).attr("data-last-name")); // make this their first name and last name
    $("#new-message-form").dialog("open");
}

function messageDeleteListener() {
    if (confirm("Do you really want to delete this message?")) {
        var message = $(this).parent().parent().parent().parent().parent();
        message.fadeOut("fast");
        $.post("/messages/delete", { "mid": message.attr("data-mid") }, function(data) {
            if (data.success == 0) { message.remove(); }
            else if (data.success == 1) { alert("Your account must be paired and opted-in in order to delete messages. Redirecting to settings page to resolve the issue..."); window.location='/settings'; }
            else if (data.success == 2) { message.remove(); alert("Message does not exist or you tried to delete another user's message."); }
	    else if (data.success == 6) { alert("Sorry. Last Chance Dance has closed and you are not allowed to delete messages anymore. Redirecting..."); window.location='/'; }
            else { message.show(); alert("Error in deleting message. Try again."); }
            checkNoMessages();
        }, "json");
    }
}

function showMessages(tab) {
    $(".messages-tab").hide();
    $("#messages-" + tab).show();
    $("#messages-nav li").removeClass("active");
    $("#messages-nav-" + tab).addClass("active");
    createCookie("tabSelection", tab);
}

function messageReplyListener() {
    messageItem = $(this).parent().parent().parent().parent();
    messageItem.next(".reply-box").show();
    messageItem.next(".reply-box").find("input").focus(); // bug here that causes hitting enter to send many replies
    messageItem.find(".reply-button").each(function() { $(this).remove(); });
    messageItem.find(".message-item-body").each(function() { $(this).css("width","22em"); });
}

function messageSendReplyListener(event) {
    if (event.keyCode == 13) {
      var message_id = $(this).parent().parent().attr("data-mid");
      var body = $(this).val();
      if (body) {
        $(this).val("");
        $(this).parent().before('<div class="message-item sent reply"><div class="message-item-header"><div class="message-item-info"><strong>You</strong> just now</div></div><div class="message-item-body">' + body + '</div></div>');
        $.post("/messages/reply", { "mid": message_id, "body": body }, function(data) {
          if (data.success == 0) { }
          else if (data.success == 1) { alert("Your account must be paired and opted-in in order to reply to messages. Redirecting to settings page to resolve the issue..."); window.location='/settings'; }
          else if (data.success == 2) { alert("Message does not exist or you tried to reply another user's message. The added reply will be gone when you refresh the page."); }
          else if (data.success == 3) { alert("Reply not sent because there was no text to send. The added reply will be gone when you refresh the page."); }
	  else if (data.success == 6) { alert("Sorry. Last Chance Dance has closed and you are not allowed to reply to messages anymore. Redirecting..."); window.location='/'; }
          else { alert("Error in replying to  message. Try again. The added reply will be gone when you refresh the page."); }
        }, "json");
      }
    }
}

function reportUserListener() {
    var message_id = $(this).parent().parent().parent().parent().parent().attr("data-mid");
    if (confirm("Do you really want to report this user?")) {
	$.post("/messages/report_abuse", { "mid": message_id }, function(data) {
	    if (data.success == 0) { alert("This user has been reported. Thank you."); }
	    else if (data.success == 1) { alert("Your account must be paired and opted-in in order to report abuse. Redirecting to settings page to resolve the issue..."); window.location='/settings'; }
	    else if (data.success == 2) { alert("Message does not exist or you tried to report abuse on another user's message. Abuse report not sent."); }
	    else if (data.success == 6) { alert("Sorry. Last Chance Dance has closed and you are not allowed to report abuse since no one can send messages anyways. Redirecting..."); window.location='/'; }
	    else { alert("Error in reporting user. Try again."); }
	    }, "json");
    }
}

function updateMessages() {
    $.get('/messages/get', function(data) {
        if (data.success == 0 && (data.num_unread_messages > 0 || data.num_unread_sent_messages)) {
            var text;
            if (data.num_unread_messages + data.num_unread_sent_messages == 1) { text = "1 unread message"; }
            else { text = (data.num_unread_messages + data.num_unread_sent_messages).toString() + " unread messages"; }
            $("#crushes-tab span").html('you have ' + text + '. <a href="/crushes">reload!</a>');
            $("#crushes-tab").addClass("alert");
            $("#crushes-tab span").fadeIn("fast");
        }
	else if (data.success == 1) { alert("Your account must be paired and opted-in in order to reply to messages. Redirecting to settings page to resolve the issue..."); window.location='/settings'; }
        setTimeout('updateMessages()', 10000);
    }, "json");   
}

function checkNoMessages() {
    if ($("#messages-to-me .messages .message").length == 0) { $("#messages-to-me .no-messages").fadeIn("fast"); }
    else { $("#messages-to-me .no-messages").fadeOut("fast"); }
    
    if ($("#messages-from-me .messages .message").length == 0) { $("#messages-from-me .no-messages").fadeIn("fast"); }
    else { $("#messages-from-me .no-messages").fadeOut("fast"); }
}

function checkNoCrushes() {
    if ($("#crushes .crushdiv").length == 0) { $("#crushes .no-crushes").fadeIn("fast"); }
    else { $("#crushes .no-crushes").fadeOut("fast"); }
}

function createCookie(name, value, days) {
	if (days) {
		var date = new Date();
		date.setTime(date.getTime()+(days*24*60*60*1000));
		var expires = "; expires="+date.toGMTString();
	}
	else var expires = "";
	document.cookie = name + "=" + value + expires + "; path=/";
}

function readCookie(name) {
	var nameEQ = name + "=";
	var ca = document.cookie.split(';');
	for(var i=0;i < ca.length;i++) {
		var c = ca[i];
		while (c.charAt(0)==' ') c = c.substring(1,c.length);
		if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
	}
	return null;
}

function eraseCookie(name) {
	createCookie(name,"",-1);
}