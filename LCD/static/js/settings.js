/* 
 * settings.js
 * Last Chance Dance 2011
 */

/*global window, $ */

/* FUNCTIONS */

function focusGetInvite() { $('#invite-form input[name="carletonID"]').focus(); }
function setAlert(text) {
    $('#response .alert').text(text);
    $('#response').fadeIn('fast');
}

function sendInvitation() {
    $.post('/settings/invite', { 'carletonID': $('#invite-form input[name="carletonID"]').val() }, function(data) {
        if (data.success === 0) { setAlert('Invitation Sent! Check Your Carleton Email.'); }
        else if (data.success === 1) { setAlert('Our database does have your username. Send us an email and convince us that you are a senior.'); }
        else if (data.success === 2) { setAlert('Last Chance Dance is not open yet. Redirecting...'); window.location='/'; }
        else { setAlert('Error in sending invite. Try again. Send us an email if you continue to have problems.'); }
    }, 'json');
}