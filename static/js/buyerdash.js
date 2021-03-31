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

  $('#checkout').click(function (e) {
    e.preventDefault();
    // var id = this.id;
    console.log("Checkout clicked");
    checkout_items();
  });

  $.ajax({
    url: '/api/buyer/cart',
    type: 'GET',
    async: true,
    statusCode: {
      200: function (msg) {
        console.log("Success");
        console.log(msg);
        var data = msg.data;
        console.log(data);
        var tbody = document.querySelector("#cartrow");
        var template = document.querySelector('#cart-template');
        data.forEach((item, i) => {
          var clone = template.content.cloneNode(true);
          var strong = clone.querySelectorAll("strong");
          strong[0].textContent = item.name;
          var i = clone.querySelectorAll("i");
          i[0].textContent = item.price;
          var h6 = clone.querySelectorAll("h6");
          h6[0].textContent = item.date;
          h6[1].textContent = item.seller;
          var button = clone.querySelectorAll("button");
          button[0].setAttribute('id', item._id.$oid);
          tbody.appendChild(clone);
        });
        $('.pdel').click(function (e) {
          e.preventDefault();
          var id = this.id;
          console.log(id);
          delete_item(id);
        });
      },
      500: function (msq) {
        console.log("Internal Server Error");
        alert("Server Error. Please try again later.");
      }
    }
  });

  $.ajax({
    url: '/api/buyer/orders',
    type: 'GET',
    async: true,
    statusCode: {
      200: function (msg) {
        console.log("Success");
        console.log(msg);
        var data = msg.data;
        console.log(data);
        var tbody = document.querySelector("#orderrow");
        var template = document.querySelector('#order-template');
        data.forEach((item, i) => {
          var clone = template.content.cloneNode(true);
          var strong = clone.querySelectorAll("strong");
          strong[0].textContent = item.name;
          var i = clone.querySelectorAll("i");
          i[0].textContent = item.price;
          var h6 = clone.querySelectorAll("h6");
          h6[0].textContent = item.date;
          h6[1].textContent = item.seller;
          tbody.appendChild(clone);
        });
        $('.pdel').click(function (e) {
          e.preventDefault();
          var id = this.id;
          console.log(id);
          delete_item(id);
        });
      },
      500: function (msq) {
        console.log("Internal Server Error");
        alert("Server Error. Please try again later.");
      }
    }
  });

  function delete_item(data) {
    $.ajax({
      url: '/api/item',
      type: 'DELETE',
      data: JSON.stringify({ 'item_id': data }),
      contentType: 'application/json; charset=utf-8',
      dataType: 'json',
      async: true,
      statusCode: {
        200: function () {
          console.log("Success");
          alert("Deleted Item from Cart");
          location.reload();
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


  function checkout_items(data) {
    $.ajax({
      url: '/api/checkout',
      type: 'POST',
      contentType: 'application/json; charset=utf-8',
      async: true,
      statusCode: {
        200: function () {
          console.log("Success");
          alert("Successfully checked out");
          location.reload();
        },
        403: function () {
          console.log("login");
          alert("Please login as a buyer");
        },
        400: function () {
          console.log("empty");
          alert("Your cart is empty!");
        },
        500: function () {
          console.log("Internal Server Error");
          alert("Server Error. Please try again later.");
        }
      }
    });
  }


});
