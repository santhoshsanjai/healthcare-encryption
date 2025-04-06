from pymongo import MongoClient

MONGO_URI = "mongodb+srv://sanjaisanthosh:ss7708402001@nodeapicluster0.h6mud9z.mongodb.net/?retryWrites=true&w=majority&appName=nodeAPICluster0" 
client = MongoClient(MONGO_URI)
db = client["healthsecure"]
# Collections
patients_collection = db["patient_collection"]
users_collection = db["users"]


print("Databases:", client.list_database_names())
print("Collections in 'healthsecure':", db.list_collection_names())