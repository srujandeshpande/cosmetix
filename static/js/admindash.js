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

$.ajax({
  url: '/api/products/unapproved/',
  type: 'GET',
  async: true,
  statusCode: {
    200: function(msg) {
      console.log("Success");
      console.log(msg);
      var data = msg.data;
      console.log(data);
      var tbody = document.querySelector("#u-prodrow");
      var template = document.querySelector('#u-ptemplate');
      data.forEach((item, i) => {
        var clone = template.content.cloneNode(true);
        var name = clone.querySelectorAll("#u-name");
          name[0].textContent = item.name;
          var cat = clone.querySelectorAll("#u-category");
          cat[0].textContent = item.category;

          var image = clone.querySelectorAll("#u-image");
          if (item.picture) {
            image[0].setAttribute("src", item.picture);
          }

          var price = clone.querySelectorAll("#u-price");
          price[0].textContent = item.price;

          var quantity = clone.querySelectorAll("#u-quantity");
          quantity[0].textContent = item.quantity;

          var desc = clone.querySelectorAll("#u-description");
          desc[0].textContent = item.description;
          var seller = clone.querySelectorAll("#u-seller");
          seller[0].textContent = item.seller;
        var button = clone.querySelectorAll("button");
        button[0].setAttribute('id', item._id.$oid);
        tbody.appendChild(clone);
      });
      $('.abut').click(function (e) {
          e.preventDefault();
          var id = this.id;
          console.log(id);
          approve_prod(id);
      });
    },
    500: function(msq) {
      console.log("Internal Server Error");
      alert("Server Error. Please try again later.");
    }
  }
});


$.ajax({
    url: '/api/get_all_products',
    type: 'GET',
    async: true,
    statusCode: {
      200: function(msg) {
        console.log("Success");
        console.log(msg);
        var data = msg.data;
        console.log(data);
        var tbody = document.querySelector("#a-prodrow");
        var template = document.querySelector('#a-ptemplate');
        data.forEach((item, i) => {
          var clone = template.content.cloneNode(true);
          var name = clone.querySelectorAll("#a-name");
            name[0].textContent = item.name;
            var cat = clone.querySelectorAll("#a-category");
            cat[0].textContent = item.category;
  
            var image = clone.querySelectorAll("#a-image");
            if (item.picture) {
              image[0].setAttribute("src", item.picture);
            }
  
            var price = clone.querySelectorAll("#a-price");
            price[0].textContent = item.price;
  
            var quantity = clone.querySelectorAll("#a-quantity");
            quantity[0].textContent = item.quantity;
  
            var desc = clone.querySelectorAll("#a-description");
            desc[0].textContent = item.description;
            var seller = clone.querySelectorAll("#a-seller");
            seller[0].textContent = item.seller;
          var button = clone.querySelectorAll("button");
          button[0].setAttribute('id', item._id.$oid);
          tbody.appendChild(clone);
        });
        $('.dbut').click(function (e) {
            e.preventDefault();
            var id = this.id;
            console.log(id);
            delete_prod(id);
        });
      },
      500: function(msq) {
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
    200: function(msg) {
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
    500: function(msq) {
      console.log("Internal Server Error");
      alert("Server Error. Please try again later.");
    }
  }
});

function delete_prod(data){
  $.ajax({
    url: '/api/delete_product/',
    type: 'DELETE',
    data: JSON.stringify({'product_id':data}),
    contentType: 'application/json; charset=utf-8',
    dataType: 'json',
    async: true,
    statusCode: {
      200: function() {
        console.log("Success");
        alert("Product Successfully Deleted");
        location.reload()
      },
      500: function() {
        console.log("Internal Server Error");
        alert("Server Error. Please try again later.");
      }
    }
  });
}

function approve_prod(data){
    $.ajax({
      url: '/api/product/approve/',
      type: 'PUT',
      data: JSON.stringify({'product_id':data}),
      contentType: 'application/json; charset=utf-8',
      dataType: 'json',
      async: true,
      statusCode: {
        200: function() {
          console.log("Success");
          alert("Product Successfully Approved");
          location.reload()
        },
        500: function() {
          console.log("Internal Server Error");
          alert("Server Error. Please try again later.");
        }
      }
    });
  }

});
