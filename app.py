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


app = Flask(__name__)
CORS(app)

app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.secret_key = b"\xd2(*K\xa0\xa8\x13]g\x1e9\x88\x10\xb0\xe0\xcc"

mongo = pymongo.MongoClient(
    "mongodb+srv://admin:admin@cluster0-dlnod.gcp.mongodb.net/test?retryWrites=true&w=majority",
    maxPoolSize=50,
    connect=True,
)
db = pymongo.database.Database(mongo, "vyapara")


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


class shopping_cart(FlaskView):

    # @app.route("/api/add_new_sale", methods=["POST"])

    # Add to shopping cart
    # AddItem()
    def post(self):
        inputData = request.json
        Product_Data = pymongo.collection.Collection(db, "Product_Data")
        Sales_Data = pymongo.collection.Collection(db, "Sales_Data")
        today = date.today()
        if "role" in session and session["role"] == "buyer":
            info = json.loads(
                dumps(Product_Data.find_one({"_id": ObjectId(inputData["product_id"])}))
            )
            Sales_Data.insert_one(
                {
                    "product": inputData["product_id"],
                    "buyer": session["email"],
                    "date": str(today.strftime("%b-%d-%Y")),
                    "price": info["price"],
                    "seller": info["seller"],
                    "name": info["name"],
                }
            )
            return Response(status=200)
        return Response(status=403)


Customer.register(app, route_base="/")
user.register(app)
shopping_cart.register(app)


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
        return render_template("admin_portal.html")


@app.route("/seller_login")
def seller_login():
    if "role" in session and session["role"] == "seller":
        return render_template("seller_dash.html")
    else:
        return render_template("seller_login.html")


# @app.route("/buyer_dash")
# def buyer_dash():
#     if "role" in session and session["role"] == "buyer":
#         return render_template("buyer_dash.html")
#     else:
#         return render_template("login_buyer.html")


@app.route("/seller_dash")
def seller_dash():
    if "role" in session and session["role"] == "seller":
        return render_template("seller_dash.html")
    else:
        return render_template("seller_login.html")


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
    return Response(status=200)


@app.route("/api/new_seller", methods=["POST"])
def new_seller():
    inputData = request.json
    Seller_Data = pymongo.collection.Collection(db, "Seller_Data")
    sellers = json.loads(dumps(Seller_Data.find()))
    if len(sellers) != 0:
        for i in sellers:
            if i["email"] == inputData["email"]:
                return Response(status=401)
    Seller_Data.insert_one(
        {"email": inputData["email"], "password": inputData["password"]}
    )
    return Response(status=200)


# @app.route("/api/login_buyer", methods=["POST"])
# def login_buyer():
#     inputData = request.json
#     Buyer_Data = pymongo.collection.Collection(db, "Buyer_Data")
#     buyers = json.loads(dumps(Buyer_Data.find()))
#     if len(buyers) == 0:
#         return Response(status=401)
#     for i in buyers:
#         if i["email"] == inputData["email"]:
#             if i["password"] == inputData["password"]:
#                 session["role"] = "buyer"
#                 session["email"] = i["email"]
#                 return Response(status=200)
#             else:
#                 return Response(status=403)
#     return Response(status=401)


@app.route("/api/login_seller", methods=["POST"])
def login_seller():
    inputData = request.json
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


@app.route("/api/add_new_product", methods=["POST"])
def add_new_product():
    inputData = request.json
    Product_Data = pymongo.collection.Collection(db, "Product_Data")
    if "role" in session and session["role"] == "seller":
        Product_Data.insert_one(
            {
                "seller": session["email"],
                "name": inputData["name"],
                "price": inputData["price"],
                "description": inputData["description"],
            }
        )
        return Response(status=200)
    return Response(status=403)


# @app.route("/api/add_new_sale", methods=["POST"])
# def add_new_sale():
#     inputData = request.json
#     Product_Data = pymongo.collection.Collection(db, "Product_Data")
#     Sales_Data = pymongo.collection.Collection(db, "Sales_Data")
#     today = date.today()
#     if "role" in session and session["role"] == "buyer":
#         info = json.loads(
#             dumps(Product_Data.find_one({"_id": ObjectId(inputData["product_id"])}))
#         )
#         Sales_Data.insert_one(
#             {
#                 "product": inputData["product_id"],
#                 "buyer": session["email"],
#                 "date": str(today.strftime("%b-%d-%Y")),
#                 "price": info["price"],
#                 "seller": info["seller"],
#                 "name": info["name"],
#             }
#         )
#         return Response(status=200)
#     return Response(status=403)


@app.route("/api/item", methods=["DELETE"])
def delete_from_cart():
    inputData = request.json
    Product_Data = pymongo.collection.Collection(db, "Product_Data")
    Sales_Data = pymongo.collection.Collection(db, "Sales_Data")
    today = date.today()
    if "role" in session and session["role"] == "buyer":
        Sales_Data.delete_one({"_id": ObjectId(inputData["item_id"])})
        return Response(status=200)
    return Response(status=403)


@app.route("/api/get_all_products")
def get_products():
    Product_Data = pymongo.collection.Collection(db, "Product_Data")
    data = json.loads(dumps(Product_Data.find()))
    data2 = {"count": len(data), "data": data}
    return data2


@app.route("/api/get_seller_products")
def get_seller_products():
    Product_Data = pymongo.collection.Collection(db, "Product_Data")
    data = json.loads(dumps(Product_Data.find({"seller": session["email"]})))
    data2 = {"count": len(data), "data": data}
    return data2


@app.route("/api/get_seller_orders")
def get_seller_orders():
    Order_Data = pymongo.collection.Collection(db, "Order_Data")
    data = json.loads(dumps(Order_Data.find({"seller": session["email"]})))
    data2 = {"count": len(data), "data": data}
    return data2


@app.route("/api/buyer/cart")
def get_buyer_cart():
    Sales_Data = pymongo.collection.Collection(db, "Sales_Data")
    data = json.loads(dumps(Sales_Data.find({"buyer": session["email"]})))
    data2 = {"count": len(data), "data": data}
    return data2


@app.route("/api/buyer/orders")
def get_buyer_orders():
    Order_Data = pymongo.collection.Collection(db, "Order_Data")
    data = json.loads(dumps(Order_Data.find({"buyer": session["email"]})))
    data2 = {"count": len(data), "data": data}
    return data2


@app.route("/api/checkout", methods=["POST"])
def checkout_items():
    Sales_Data = pymongo.collection.Collection(db, "Sales_Data")
    Order_Data = pymongo.collection.Collection(db, "Order_Data")
    data = json.loads(dumps(Sales_Data.find({"buyer": session["email"]}, {"_id": 0})))
    # print(data)
    if len(data) == 0:
        return Response(status=400)
    if "role" in session and session["role"] == "buyer":
        Order_Data.insert_many(data)
        Sales_Data.delete_many({"buyer": session["email"]})
        return Response(status=200)
    return Response(status=403)


@app.route("/api/delete_product", methods=["POST"])
def delete_product():
    inputData = request.json
    Product_Data = pymongo.collection.Collection(db, "Product_Data")
    if "role" in session and session["role"] == "seller":
        Product_Data.delete_one({"_id": ObjectId(inputData["product_id"])})
        return Response(status=200)
    return Response(status=403)
