$(function () {

    function logout() {
        $.ajax({
            url: '/api/logout',
            type: 'POST',
            async: true,
            statusCode: {
                200: function () {
                    console.log("Success");
                    document.location.href = '/'
                }
            }
        });
    }

    $('#logout-button').click(function (e) {
        e.preventDefault();
        logout();
    });

});
