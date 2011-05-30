function inviteAll() {
    if (confirm('Do you really want to send invites to everyone?')) {
        $.get('/admin/invite_all', function(data) {
            if (data.success == 0) { alert('Invites sent.'); }
            else { alert('Error sending invites.'); }
        }, 'json');
    }
}

function inviteNotPaired() {
    if (confirm('Do you really want to send invites to everyone who has not paired their acccount?')) {
        $.get('/admin/invite_not_paired', function(data) {
            if (data.success == 0) { alert('Invites to unpaired users sent.'); }
            else { alert('Error sending invites.'); }
        }, 'json');
    }
}

function updateStatistics() {
    $.get('/tasks/update_statistics', function(data) {
        if (data.success == 0) { alert('Statistics updated.'); }
        else { alert('Error updating statistics.'); }
    }, 'json');
}

function sendMatchNotifications() {
    if (confirm('Do you really want to send match notifications to everyone?')) {
        $.get('/admin/send_match_notifications', function(data) {
            if (data.success == 0) { alert('Match notifications sent! We\'ll see what happens next!'); }
            else { alert('Error sending match notifications.'); }
        }, 'json');
    }
}

function setSiteStatus() {
    if (confirm('Do you really want to change the site status?')) {
        $.post('/admin/set_site_status', { 'site_status': $('input[name="site_status"]:checked').val() }, function(data) {
            if (data.success == 0) { alert('Site status successfully changed to ' + data.status + "."); }
            else if (data.success == 1) { alert('Not a valid site status value: ' + data.status + "."); }
            else { alert('Error changing site status.'); }
            window.location.reload();
        }, 'json');
    }
}