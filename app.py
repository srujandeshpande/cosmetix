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


@app.route("/api/test")
def test():
    return "Works"


@app.route("/")
def homepage():
    return render_template("index.html")
