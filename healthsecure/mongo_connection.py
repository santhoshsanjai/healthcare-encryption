from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["healthcare_db"]

# Collections
patients_collection = db["patient_collection"]
users_collection = db["users"]