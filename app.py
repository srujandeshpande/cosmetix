# IMPORTS
import pymongo
from bson.json_util import dumps
import json
from flask import (
    Flask,
    request,
    render_template,
    session,
    redirect,
    url_for,
    flash,
    Response,
    abort,
    render_template_string,
    send_from_directory,
)
from flask_cors import CORS
import requests
from datetime import date
from bson.objectid import ObjectId
from flask_classful import FlaskView, route

# App constants

app = Flask(__name__)
CORS(app)

app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.secret_key = b"\xd2(*K\xa0\xa8\x13]g\x1e9\x88\x10\xb0\xe0\xcc"

# Database connection

mongo = pymongo.MongoClient(
    "mongodb+srv://admin:admin@cluster0-dlnod.gcp.mongodb.net/test?retryWrites=true&w=majority",
    maxPoolSize=50,
    connect=True,
)
db = pymongo.database.Database(mongo, "vyapara")

# Customer Class


class Customer(FlaskView):
    default_methods = ["GET", "POST"]

    def buyer_login(self):
        return render_template("login_buyer.html")

    def buyer_new(self):
        return render_template("new_buyer.html")

    def buyer_dash(self):
        if "role" in session and session["role"] == "buyer":
            return render_template("buyer_dash.html")
        else:
            return render_template("login_buyer.html")


class user(FlaskView):
    # @route("/api/login_buyer")

    # Login User (Customer)
    def post(self):
        inputData = request.json
        Buyer_Data = pymongo.collection.Collection(db, "Buyer_Data")
        buyers = json.loads(dumps(Buyer_Data.find()))
        if len(buyers) == 0:
            return Response(status=401)
        for i in buyers:
            if i["email"] == inputData["email"]:
                if i["password"] == inputData["password"]:
                    session["role"] = "buyer"
                    session["email"] = i["email"]
                    return Response(status=200)
                else:
                    return Response(status=403)
        return Response(status=401)


Customer.register(app, route_base="/")
user.register(app)


@app.route("/api/test")
def test():
    return "Works"


@app.route("/")
def homepage():
    return render_template("index.html")


@app.route("/api/logout", methods=["POST"])
def logout():
    session.clear()
    return Response(status=200)


# @app.route('/buyer_login')
# def buyer_login():
#     return (render_template('login_buyer.html'))


# @app.route("/buyer_new")
# def buyer_new():
#     return render_template("new_buyer.html")


@app.route("/admin")
def admin_portal():
    session["role"] = "admin"
    session["email"] = "admin@admin.com"
    return render_template("admin_portal.html")


@app.route("/api/new_buyer", methods=["POST"])
def new_buyer():
    inputData = request.json
    Buyer_Data = pymongo.collection.Collection(db, "Buyer_Data")
    buyers = json.loads(dumps(Buyer_Data.find()))
    if len(buyers) != 0:
        for i in buyers:
            if i["email"] == inputData["email"]:
                return Response(status=401)
    Buyer_Data.insert_one(
        {"email": inputData["email"], "password": inputData["password"]}
    )
    session["role"] = "buyer"
    session["email"] = inputData["email"]
    return Response(status=200)


class Vendor:
    def seller_login():
        if "role" in session and session["role"] == "seller":
            return render_template("seller_dash.html")
        else:
            return render_template("seller_login.html")

    def seller_dash():
        if "role" in session and session["role"] == "seller":
            return render_template("seller_dash.html")
        else:
            return render_template("seller_login.html")

    def new_seller(inputData):
        Seller_Data = pymongo.collection.Collection(db, "Seller_Data")
        sellers = json.loads(dumps(Seller_Data.find()))
        if len(sellers) != 0:
            for i in sellers:
                if i["email"] == inputData["email"]:
                    return Response(status=401)
        Seller_Data.insert_one(
            {"email": inputData["email"], "password": inputData["password"]}
        )
        session["role"] = "seller"
        session["email"] = inputData["email"]
        return Response(status=200)

    def login_seller(inputData):
        Seller_Data = pymongo.collection.Collection(db, "Seller_Data")
        sellers = json.loads(dumps(Seller_Data.find()))
        if len(sellers) == 0:
            return Response(status=401)
        for i in sellers:
            if i["email"] == inputData["email"]:
                if i["password"] == inputData["password"]:
                    session["role"] = "seller"
                    session["email"] = i["email"]
                    return Response(status=200)
                else:
                    return Response(status=403)
        return Response(status=401)

    def all_products():
        Product_Data = pymongo.collection.Collection(db, "Product_Data")
        data = json.loads(dumps(Product_Data.find({"seller": session["email"]})))
        data2 = {"count": len(data), "data": data}
        return data2

    def get_single_product(inputData):
        Product_Data = pymongo.collection.Collection(db, "Product_Data")
        data = json.loads(
            dumps(Product_Data.find_one({"_id": ObjectId(inputData["product_id"])}))
        )
        return data

    def get_seller_orders():
        Order_Data = pymongo.collection.Collection(db, "Order_Data")
        data = json.loads(dumps(Order_Data.find({"seller": session["email"]})))
        data2 = {"count": len(data), "data": data}
        return data2


# Start Vendor Class Routes


@app.route("/seller_login")
def seller_login():
    return Vendor.seller_login()


@app.route("/seller_dash")
def seller_dash():
    return Vendor.seller_dash()


@app.route("/api/new_seller", methods=["POST"])
def new_seller():
    inputData = request.json
    return Vendor.new_seller(inputData)


@app.route("/api/login_seller", methods=["POST"])
def login_seller():
    inputData = request.json
    return Vendor.login_seller(inputData)


@app.route("/api/seller/products")
def get_seller_products():
    return Vendor.all_products()


@app.route("/api/seller/product/", methods=["POST"])
def get_seller_product():
    inputData = request.json
    return Vendor.get_single_product(inputData)


@app.route("/api/seller/orders")
def get_seller_orders():
    return Vendor.get_seller_orders()


# End Vendor Class Routes


class Inventory:
    def new_product(inputData):
        Product_Data = pymongo.collection.Collection(db, "Product_Data")
        if "role" in session and session["role"] == "seller":
            inputData["quantity"] = int(inputData["quantity"])
            inputData["seller"] = session["email"]
            inputData["approved"] = False
            Product_Data.insert_one(inputData)
            return Response(status=200)
        return Response(status=403)

    def edit_product(inputData):
        Product_Data = pymongo.collection.Collection(db, "Product_Data")
        if "role" in session and session["role"] == "seller":
            inputData["quantity"] = int(inputData["quantity"])
            # inputData["_id"] = ObjectId(inputData["_id"])
            id = ObjectId(inputData.pop("_id"))
            print(inputData)
            Product_Data.update_one({"_id": id}, {"$set": inputData})
            return Response(status=200)
        return Response(status=403)

    def available_products():
        Product_Data = pymongo.collection.Collection(db, "Product_Data")
        data = json.loads(
            dumps(Product_Data.find({"approved": True, "quantity": {"$gt": 0}}))
        )
        data2 = {"count": len(data), "data": data}
        return data2

    def all_products():
        Product_Data = pymongo.collection.Collection(db, "Product_Data")
        data = json.loads(dumps(Product_Data.find({"approved": True})))
        data2 = {"count": len(data), "data": data}
        return data2


# Start Inventory Class Routes


@app.route("/api/product", methods=["POST"])
def add_new_product():
    inputData = request.json
    return Inventory.new_product(inputData)


@app.route("/api/product/edit/", methods=["PUT"])
def edit_product():
    inputData = request.json
    return Inventory.edit_product(inputData)


@app.route("/api/products/available/")
def get_available_products():
    return Inventory.available_products()


@app.route("/api/get_all_products")
def get_products():
    return Inventory.all_products()


# End Inventory Routes


class ShoppingCart:
    def buyer_cart():
        Sales_Data = pymongo.collection.Collection(db, "Sales_Data")
        data = json.loads(dumps(Sales_Data.find({"buyer": session["email"]})))
        data2 = {"count": len(data), "data": data}
        return data2

    def buyer_total():
        Sales_Data = pymongo.collection.Collection(db, "Sales_Data")
        data = json.loads(dumps(Sales_Data.find({"buyer": session["email"]})))
        tprice = 0
        for i in data:
            if "price" in i:
                tprice += int(i["price"])*int(i["quantity"])
        return {"price": tprice}

    def buyer_add_to_cart(inputData):
        Product_Data = pymongo.collection.Collection(db, "Product_Data")
        Sales_Data = pymongo.collection.Collection(db, "Sales_Data")
        today = date.today()
        if "role" in session and session["role"] == "buyer":
            info = json.loads(
                dumps(Product_Data.find_one({"_id": ObjectId(inputData["product_id"])}))
            )
            orderInfo = json.loads(
                dumps(Sales_Data.find_one({"product": inputData["product_id"]}))
            )
            if orderInfo:
                Sales_Data.update_one(
                    {"product": inputData["product_id"]}, {"$inc": {"quantity": 1}}
                )
            else:
                Sales_Data.insert_one(
                    {
                        "product": inputData["product_id"],
                        "buyer": session["email"],
                        "date": str(today.strftime("%b-%d-%Y")),
                        "price": info["price"],
                        "seller": info["seller"],
                        "name": info["name"],
                        "quantity": 1,
                    }
                )
            Product_Data.update_one(
                {"_id": ObjectId(inputData["product_id"])}, {"$inc": {"quantity": -1}}
            )
            return Response(status=200)
        return Response(status=403)

    def buyer_checkout():
        Sales_Data = pymongo.collection.Collection(db, "Sales_Data")
        Order_Data = pymongo.collection.Collection(db, "Order_Data")
        data = json.loads(
            dumps(Sales_Data.find({"buyer": session["email"]}, {"_id": 0}))
        )
        if len(data) == 0:
            return Response(status=400)
        if "role" in session and session["role"] == "buyer":
            Order_Data.insert_many(data)
            Sales_Data.delete_many({"buyer": session["email"]})
            return Response(status=200)
        return Response(status=403)

    def buyer_orders():
        Order_Data = pymongo.collection.Collection(db, "Order_Data")
        data = json.loads(dumps(Order_Data.find({"buyer": session["email"]})))
        data2 = {"count": len(data), "data": data}
        return data2

    def buyer_delete_from_cart(inputData):
        Product_Data = pymongo.collection.Collection(db, "Product_Data")
        Sales_Data = pymongo.collection.Collection(db, "Sales_Data")
        today = date.today()
        if "role" in session and session["role"] == "buyer":
            data = json.loads(
                dumps(Sales_Data.find_one({"_id": ObjectId(inputData["item_id"])}))
            )
            Sales_Data.delete_one({"_id": ObjectId(inputData["item_id"])})
            Product_Data.update_one(
                {"_id": ObjectId(data["product"])},
                {"$inc": {"quantity": int(data["quantity"])}},
            )
            return Response(status=200)
        return Response(status=403)

    def buyer_update_cart_quantity(inputData):
        Product_Data = pymongo.collection.Collection(db, "Product_Data")
        Sales_Data = pymongo.collection.Collection(db, "Sales_Data")
        today = date.today()
        if "role" in session and session["role"] == "buyer":
            data = json.loads(
                dumps(Sales_Data.find_one({"_id": ObjectId(inputData["item_id"])}))
            )
            proddata = json.loads(
                dumps(Product_Data.find_one({"_id": ObjectId(data["product"])}))
            )
            if int(data["quantity"]) == 1 and int(inputData["n"]) == -1:
                Sales_Data.delete_one({"_id": ObjectId(inputData["item_id"])})
                Product_Data.update_one(
                    {"_id": ObjectId(data["product"])},
                    {"$inc": {"quantity": int(data["quantity"])}},
                )
            elif int(inputData["n"]) == 1 and int(proddata["quantity"]) == 0:
                return Response(status=401)
            else:
                Sales_Data.update_one(
                    {"_id": ObjectId(inputData["item_id"])},
                    {"$inc": {"quantity": int(inputData["n"])}},
                )
                Product_Data.update_one(
                    {"_id": ObjectId(data["product"])},
                    {"$inc": {"quantity": -int(inputData["n"])}},
                )
            return Response(status=200)
        return Response(status=403)


# Start Routes for Shopping Cart Class


@app.route("/api/buyer/cart")
def get_buyer_cart():
    return ShoppingCart.buyer_cart()


@app.route("/api/buyer/total/")
def get_buyer_total():
    return ShoppingCart.buyer_total()


@app.route("/api/buyer/cart/add/", methods=["POST"])
def add_to_cart():
    inputData = request.json
    return ShoppingCart.buyer_add_to_cart(inputData)


@app.route("/api/checkout", methods=["POST"])
def checkout_items():
    return ShoppingCart.buyer_checkout()


@app.route("/api/buyer/orders")
def get_buyer_orders():
    return ShoppingCart.buyer_orders()


@app.route("/api/cart/item/", methods=["DELETE"])
def delete_from_cart():
    inputData = request.json
    return ShoppingCart.buyer_delete_from_cart(inputData)


@app.route("/api/cart/quantity/", methods=["POST"])
def update_cart_quantity():
    inputData = request.json
    return ShoppingCart.buyer_update_cart_quantity(inputData)


# End Routes for Shopping Cart Class


class Admin:
    def approve_product(inputData):
        Product_Data = pymongo.collection.Collection(db, "Product_Data")
        if "role" in session and session["role"] == "admin":
            Product_Data.update_one(
                {"_id": ObjectId(inputData["product_id"])}, {"$set": {"approved": True}}
            )
            return Response(status=200)
        return Response(status=403)

    def delete_product(inputData):
        Product_Data = pymongo.collection.Collection(db, "Product_Data")
        if "role" in session and (
            session["role"] == "seller" or session["role"] == "admin"
        ):
            Product_Data.delete_one({"_id": ObjectId(inputData["product_id"])})
            return Response(status=200)
        return Response(status=403)

    def unapproved_products():
        Product_Data = pymongo.collection.Collection(db, "Product_Data")
        data = json.loads(dumps(Product_Data.find({"approved": False})))
        data2 = {"count": len(data), "data": data}
        return data2


# Start Admin Routes


@app.route("/api/product/approve/", methods=["PUT"])
def approve_product():
    inputData = request.json
    return Admin.approve_product(inputData)


@app.route("/api/delete_product/", methods=["DELETE"])
def delete_product():
    inputData = request.json
    return Admin.delete_product(inputData)


@app.route("/api/products/unapproved/")
def get_products_unnapproved():
    return Admin.unapproved_products()


# End Admin Routes
