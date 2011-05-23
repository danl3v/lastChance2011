function focusGetInvite() { $("#invite-form input[name='carletonID']").focus(); }
function setAlert(text) {
    $("#response .alert").text(text);
    $("#response").fadeIn("fast");
}

function sendInvitation() {
    $.post("/settings/invite", { 'carletonID': $('#invite-form input[name="carletonID"]').val() }, function(data) {
        if (data.success == 0) { setAlert('Invitation Sent! Check your email.') }
        else if (data.success == 1) { setAlert('Our database does have your username. Send us an email and convince us that you are a senior.'); }
        else { setAlert('Error in sending invite. Try again. Send us an email if you continue to have problems.') }
    }, "json");
}