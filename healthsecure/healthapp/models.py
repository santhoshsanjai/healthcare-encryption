from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime

# ✅ MongoDB Setup
client = MongoClient("mongodb://localhost:27017/")
db = client["healthcare_db"]

# Collections
patients_collection = db["patient_collection"]
records_collection = db["patient_records"]
users_collection = db["users"]

# ✅ Patient Logic
class Patient:
    @staticmethod
    def create(name, age, diagnosis=None, health_data=None, sensitive_data=False):
        patient = {
            "name": name,
            "age": age,
            "diagnosis": diagnosis,
            "health_data": health_data or {},
            "sensitive_data": sensitive_data
        }
        result = patients_collection.insert_one(patient)
        return str(result.inserted_id)

    @staticmethod
    def get_by_id(patient_id):
        return patients_collection.find_one({"_id": ObjectId(patient_id)})

    @staticmethod
    def get_all():
        return list(patients_collection.find())

# ✅ PatientRecord Logic
class PatientRecord:
    CLASSIFICATION_CHOICES = ['Sensitive', 'Non-Sensitive']

    @staticmethod
    def create(patient_id, medical_history, classified_as, encrypted_data=None, stego_image=None):
        if classified_as not in PatientRecord.CLASSIFICATION_CHOICES:
            raise ValueError("Invalid classification")

        record = {
            "patient_id": ObjectId(patient_id),
            "medical_history": medical_history,
            "classified_as": classified_as,
            "encrypted_data": encrypted_data,
            "stego_image": stego_image,
            "created_at": datetime.utcnow()
        }
        result = records_collection.insert_one(record)
        return str(result.inserted_id)

    @staticmethod
    def get_by_patient(patient_id):
        return list(records_collection.find({"patient_id": ObjectId(patient_id)}))

    @staticmethod
    def get_all():
        return list(records_collection.find())
