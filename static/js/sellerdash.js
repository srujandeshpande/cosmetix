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
    url: '/api/seller/products',
    type: 'GET',
    async: true,
    statusCode: {
      200: function (msg) {
        console.log("Success");
        console.log(msg);
        var data = msg.data;
        console.log(data);
        var tbody = document.querySelector("#prodrow");
        var template = document.querySelector('#ptemplate');
        data.forEach((item, i) => {
          var clone = template.content.cloneNode(true);
          var name = clone.querySelectorAll("#name");
          name[0].textContent = item.name;
          var cat = clone.querySelectorAll("#category");
          cat[0].textContent = item.category;

          var image = clone.querySelectorAll("#image");
          if (item.picture) {
            image[0].setAttribute("src", item.picture);
          }

          var price = clone.querySelectorAll("#price");
          price[0].textContent = item.price;

          var quantity = clone.querySelectorAll("#quantity");
          quantity[0].textContent = item.quantity;

          var desc = clone.querySelectorAll("#description");
          desc[0].textContent = item.description;
          var button = clone.querySelectorAll(".pdel");
          button[0].setAttribute('id', item._id.$oid);
          var button = clone.querySelectorAll(".edit-btn");
          button[0].setAttribute('data-id2', item._id.$oid);
          tbody.appendChild(clone);
        });
        $('.pdel').click(function (e) {
          e.preventDefault();
          var id = this.id;
          console.log(id);
          del_prod(id);
        });
        $('.edit-btn').click(function (e) {
          var id = jQuery(this).attr('data-id2');
          console.log(id);
          edit_prod(id);
        });
      },
      500: function (msq) {
        console.log("Internal Server Error");
        alert("Server Error. Please try again later.");
      }
    }
  });

  $.ajax({
    url: '/api/seller/orders',
    type: 'GET',
    async: true,
    statusCode: {
      200: function (msg) {
        console.log("Success");
        console.log(msg);
        var data = msg.data;
        console.log(data);
        var tbody = document.querySelector("#orderrow");
        var template = document.querySelector('#otemplate');
        data.forEach((item, i) => {
          var clone = template.content.cloneNode(true);
          var strong = clone.querySelectorAll("strong");
          strong[0].textContent = item.name;
          var i = clone.querySelectorAll("i");
          i[0].textContent = item.price;
          var h6 = clone.querySelectorAll("h6");
          h6[0].textContent = item.buyer;
          h6[1].textContent = item.date;
          tbody.appendChild(clone);
        });
      },
      500: function (msq) {
        console.log("Internal Server Error");
        alert("Server Error. Please try again later.");
      }
    }
  });

  function create_new(data) {
    $.ajax({
      url: '/api/product',
      type: 'POST',
      data: JSON.stringify(data),
      contentType: 'application/json; charset=utf-8',
      dataType: 'json',
      async: true,
      statusCode: {
        200: function () {
          console.log("Success");
          alert("Successfully Added!");
          location.reload();
        },
        500: function () {
          console.log("Internal Server Error");
          alert("Server Error. Please try again later.");
        }
      }
    });
  }

  function update_prod(data) {
    $.ajax({
      url: '/api/product/edit/',
      type: 'PUT',
      data: JSON.stringify(data),
      contentType: 'application/json; charset=utf-8',
      dataType: 'json',
      async: true,
      statusCode: {
        200: function () {
          console.log("Success");
          alert("Successfully Updated!");
          location.reload();
        },
        500: function () {
          console.log("Internal Server Error");
          alert("Server Error. Please try again later.");
        }
      }
    });
  }

  $('#seller-add-new-product').submit(function (e) {
    e.preventDefault();
    var data = $(this).serializeFormJSON();
    create_new(data);
  });

  $('#edit-form').submit(function (e) {
    e.preventDefault();
    var data = $(this).serializeFormJSON();
    data['_id'] = $('#edit-id').val();
    console.log(data);
    update_prod(data);
  });

  function del_prod(data) {
    $.ajax({
      url: '/api/delete_product/',
      type: 'DELETE',
      data: JSON.stringify({ 'product_id': data }),
      contentType: 'application/json; charset=utf-8',
      dataType: 'json',
      async: true,
      statusCode: {
        200: function () {
          console.log("Success");
          alert("Product Successfully Deleted");
          location.reload()
        },
        500: function () {
          console.log("Internal Server Error");
          alert("Server Error. Please try again later.");
        }
      }
    });
  }

  function edit_prod(data) {
    $.ajax({
      url: '/api/seller/product/',
      type: 'POST',
      data: JSON.stringify({ 'product_id': data }),
      contentType: 'application/json; charset=utf-8',
      dataType: 'json',
      async: true,
      statusCode: {
        200: function (msg) {
          console.log("Success");
          $('#edit-id').val(data);
          $('#edit-name').val(msg.name);
          $('#edit-price').val(msg.price);
          $('#edit-desc').val(msg.description);
          $('#edit-quantity').val(msg.quantity);
          $('#edit-url').val(msg.picture);
        },
        500: function () {
          console.log("Internal Server Error");
          alert("Server Error. Please try again later.");
        }
      }
    });
  }

});
