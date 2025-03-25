import json
import numpy as np
from bson import ObjectId
from pymongo import MongoClient
from sklearn.svm import SVC
from cryptography.fernet import Fernet
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password, make_password
from django.contrib import messages
from mongo_connection import patients_collection, users_collection

# --------------------- 🔐 SETUP ----------------------

ENCRYPTION_KEY = b'yZ9Xk1qPl9TrB5suT3z5mLSN1Yi1jR-JK5LV5aMIb24='
cipher_suite = Fernet(ENCRYPTION_KEY)

svm_model = SVC(probability=True)
X_train = np.array([[75, 1], [120, 0]])
y_train = np.array([1, 0])
svm_model.fit(X_train, y_train)

def classify_data(data):
    heart_rate = data.get("heart_rate", 80)
    blood_pressure = sum(map(int, data.get("blood_pressure", "120/80").split('/'))) / 2
    prediction = svm_model.predict([[heart_rate, blood_pressure]])
    return bool(prediction[0])

# --------------------- 🔒 LOGIN ----------------------

@csrf_exempt
def login_view(request):
    # admin_user = {
    # "username": "admin",
    # "password": make_password("admin123"),  # Hashing the password for security
    # "role": "admin"
    # }

# Insert the admin user into the database
    # users_collection.insert_one(admin_user)
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = users_collection.find_one({"username": username})

        if user and check_password(password, user["password"]):
            request.session['username'] = user["username"]
            request.session['role'] = user["role"]

            if user["role"] == "admin":
                return redirect('add_record')
            elif user["role"] == "user":
                return redirect('records')
            else:
                messages.error(request, "Unknown role. Contact admin.")
                return redirect('login')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'login.html')

# --------------------- 🔓 LOGOUT ----------------------

def logout(request):
    request.session.flush()
    return redirect('login')

# --------------------- 🔐 LOGIN REQUIRED DECORATOR ----------------------

def login_required_view(view_func):
    def wrapper(request, *args, **kwargs):
        if 'username' not in request.session:
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

# --------------------- 🎛️ ROLE ACCESS ----------------------

def roleAccess(page, request):
    role = request.session.get('role')
    access_map = {
        'view_records': {'admin': (True, True), 'user': (True, False)},
        'add_records': {'admin': (True, False)},
        'decrpt': {'admin': (True, False), 'user': (False, False)},
        'delete': {'admin': (True, True), 'user': (False, False)}
    }

    if role and page in access_map and role in access_map[page]:
        isAccess, isDelete = access_map[page][role]
        return {'isAccess': isAccess, 'isDelete': isDelete}

    return {'isAccess': False, 'isDelete': False}

# --------------------- ➕ ADD PATIENT ----------------------

@login_required_view
def add_record(request):
    access = roleAccess('add_records', request)
    if not access['isAccess']:
        return redirect('login')

    if request.method == "POST":
        try:
            name = request.POST.get("name")
            age = request.POST.get("age", "")
            diagnosis = request.POST.get("diagnosis", "")
            raw_health_data = request.POST.get("health_data", "{}")

            try:
                age = int(age)
            except ValueError:
                messages.error(request, "Age must be a number.")
                return render(request, "add_record.html")

            try:
                health_data = json.loads(raw_health_data)
            except json.JSONDecodeError:
                messages.error(request, "Invalid JSON format in Health Data.")
                return render(request, "add_record.html")

            is_sensitive = classify_data(health_data)

            encrypted_data = (
                cipher_suite.encrypt(json.dumps(health_data).encode()).decode()
                if is_sensitive else json.dumps(health_data)
            )

            patient = {
                "name": name,
                "age": age,
                "diagnosis": diagnosis,
                "health_data": encrypted_data,
                "sensitive_data": is_sensitive
            }
            print('yes')
            patients_collection.insert_one(patient)
            messages.success(request, "Patient record added successfully!")
            return redirect('records')

        except Exception as e:
            messages.error(request, f"Error: {str(e)}")

    return render(request, "add_record.html")

# --------------------- 📋 VIEW RECORDS ----------------------

@login_required_view
def view_records(request):
    access = roleAccess('view_records', request)
    if access['isAccess']:
        patients = []
        for patient in patients_collection.find():
            patient["id"] = str(patient["_id"])
            patient["isDelete"] = access["isDelete"]
            patients.append(patient)
        return render(request, "view_records.html", {"patients": patients})
    return redirect('login')

# --------------------- ❌ DELETE PATIENT ----------------------

@login_required_view
def delete_patient(request, patient_id):
    access = roleAccess('delete', request)

    if not access['isAccess']:
        if request.session.get('username'):
            messages.error(request, "You do not have permission to delete records.")
            return redirect('records')
        return redirect('login')

    if request.method == "GET":
        try:
            result = patients_collection.delete_one({"_id": ObjectId(patient_id)})
            if result.deleted_count == 1:
                return redirect("records")
            return JsonResponse({"error": "Patient record not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return HttpResponseForbidden("Invalid request method.")

# --------------------- 🔓 DECRYPT PATIENT DATA ----------------------

@login_required_view
def decrypt_patient_data(request, patient_id):
    access = roleAccess('decrpt', request)
    if not access['isAccess']:
        return redirect('login')

    try:
        patient = patients_collection.find_one({"_id": ObjectId(patient_id)})

        if not patient:
            return JsonResponse({"error": "Patient record not found"}, status=404)

        if patient.get("sensitive_data"):
            decrypted_data = cipher_suite.decrypt(patient["health_data"].encode()).decode()
            return render(request, "decript_data.html", {
                "patients": patient,
                "decripted_data": json.dumps(json.loads(decrypted_data), indent=4)
            })

        return JsonResponse({"health_data": json.loads(patient["health_data"])})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

# --------------------- 🌐 CUSTOM 404 HANDLER ----------------------

def custom_404_view(request, exception):
    if request.session.get('username'):
        return redirect('add_record')
    else:
        return redirect('login')
