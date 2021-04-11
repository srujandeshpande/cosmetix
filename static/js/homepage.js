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

$(function () {

  $.ajax({
    url: '/api/get_all_products',
    type: 'GET',
    async: true,
    statusCode: {
      200: function (msg) {
        console.log("Success");
        console.log(msg);
        var data = msg.data;
        console.log(data);
        // var tbody = document.querySelector("#prodrow");
        var template = document.querySelector('#ptemplate');
        data.forEach((item, i) => {
          var clone = template.content.cloneNode(true);
          var name = clone.querySelectorAll("#name");
          name[0].textContent = item.name;
          var cat = clone.querySelectorAll("#category");
          cat[0].textContent = item.category;
          var catid = "#"+item.category.toLowerCase()+"-row";

          var image = clone.querySelectorAll("#image");
          if (item.picture) {
            image[0].setAttribute("src", item.picture);
          }


          var price = clone.querySelectorAll("#price");
          price[0].textContent = item.price;

          var desc = clone.querySelectorAll("#description");
          desc[0].textContent = item.description;
          var seller = clone.querySelectorAll("#seller");
          seller[0].textContent = item.seller;

          var button = clone.querySelectorAll("button");
          button[0].setAttribute('id', item._id.$oid);

          var trow = document.querySelector(catid);
          trow.appendChild(clone);
        });
        $('.pbuy').click(function (e) {
          e.preventDefault();
          var id = this.id;
          console.log(id);
          new_order(id);
        });
      },
      500: function (msq) {
        console.log("Internal Server Error");
        alert("Server Error. Please try again later.");
      }
    }
  });

  function new_order(data) {
    $.ajax({
      url: '/shopping_cart/',
      type: 'POST',
      data: JSON.stringify({ 'product_id': data }),
      contentType: 'application/json; charset=utf-8',
      dataType: 'json',
      async: true,
      statusCode: {
        200: function () {
          console.log("Success");
          alert("Added to cart!");
        },
        403: function () {
          console.log("login");
          alert("Please login as a buyer");
        },
        500: function () {
          console.log("Internal Server Error");
          alert("Server Error. Please try again later.");
        }
      }
    });
  }

});
