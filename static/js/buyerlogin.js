(function ($) {
    $.fn.serializeFormJSON = function () {
        var o = {};
        var a = this.serializeArray();
        $.each(a, function () {
            if (this.value) {
              o[this.name] = this.value
            }
        });
        return o;
    };
})(jQuery);

$(function() {

function login(data){
  $.ajax({
    url: '/user',
    type: 'POST',
    data: JSON.stringify(data),
    contentType: 'application/json; charset=utf-8',
    dataType: 'json',
    async: true,
    statusCode: {
      200: function() {
        console.log("Success");
        document.location.href = '/'
      },
      401: function() {
        console.log("No account");
        alert("You don't have an account. Please try creating one instead.");
      },
      403: function() {
        console.log("Wrong Password");
        alert("Wrong password. Please try again.");
      },
      500: function() {
        console.log("Internal Server Error");
        alert("Server Error. Please try again later.");
      }
    }
  });
}

$('#buyer-login-form').submit(function (e) {
    e.preventDefault();
    var data = $(this).serializeFormJSON();
    login(data);
});

});
