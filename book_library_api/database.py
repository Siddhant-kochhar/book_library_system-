from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["myAppDB"]
collection = db["users"]
