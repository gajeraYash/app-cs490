function get_feed() {
    $.ajax({
        url: 'user/feed',
        type: "get",
        cache: true,
        data: {
            'feed_param': ''
        },
        dataType: 'html',
        success: function (data) {
            $('#feed-content').html(data)
        }
    });
    // 'feed_param': 'FOLLOWING'  Get USER Following Announcements
    // 'feed_param': ''  Get Self created announcements
    // 'feed_param': 'username'  Get Other user created announcements
}

$(document).ready(function () {
    get_feed();
});