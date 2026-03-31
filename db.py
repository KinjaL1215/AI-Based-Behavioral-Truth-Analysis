from pymongo import MongoClient

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")

# Database
db = client["ai_behavior_db"]

# Collections
users_collection = db["users"]

# User authentication using email
def authenticate_user_by_email(email, password):
	"""
	Authenticate user by email and password.
	Returns user document if authentication is successful, else None.
	"""
	user = users_collection.find_one({
		"email": email,
		"password": password
	})
	return user
