from pymongo import MongoClient

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")

# Database
db = client["ai_behavior_db"]

# Collections
users_collection = db["users"]
