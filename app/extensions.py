from flask_pymongo import PyMongo
from flask import Flask
# Setup MongoDB here
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/database"
mongo = PyMongo(app)