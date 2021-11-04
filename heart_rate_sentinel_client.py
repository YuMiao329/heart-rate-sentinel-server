import requests

hostname = "http://127.0.0.1:5000/"
"""
# here is Yu's hostname:
hostname = "http://vcm-23088.vm.duke.edu:5000/"
# here is Jimmy's hostname:
hostname = "http://vcm-23099.vm.duke.edu:5000/"
"""

""" New Attending """
# Successfully add new attending
attending1 = {"attending_username": "Smith.J",
              "attending_email": "dr_user_id@ourdomain.com",
              "attending_phone": "919-867-5309"}
r = requests.post(hostname + "api/new_attending", json=attending1)
print(r.status_code)
print(r.text)

attending = {"attending_username": "Ann.A",
             "attending_email": "dr_user_id@ourdomain.com",
             "attending_phone": "919-867-5309"}
r = requests.post(hostname + "api/new_attending", json=attending)
print(r.status_code)
print(r.text)

# Check for missing key
attending2 = {"attending_username": "Smith.J",
              "attending_email": "dr_user_id@ourdomain.com"}
r = requests.post(hostname + "api/new_attending", json=attending2)
print(r.status_code)
print(r.text)

# Check for bad data type
attending3 = {"attending_username": 3,
              "attending_email": "dr_user_id@ourdomain.com",
              "attending_phone": "919-867-5309"}
r = requests.post(hostname + "api/new_attending", json=attending3)
print(r.status_code)
print(r.text)

""" New Patient """
patient1 = {"patient_id": 1,
            "attending_username": "Smith.J",
            "patient_age": 50}
r = requests.post(hostname + "api/new_patient", json=patient1)
print(r.status_code)
print(r.text)

patient2 = {"patient_id": 2,
            "attending_username": "Ann.A",
            "patient_age": 40}
r = requests.post(hostname + "api/new_patient", json=patient2)
print(r.status_code)
print(r.text)

patient3 = {"patient_id": 3,
            "attending_username": "Ann.A"}
r = requests.post(hostname + "api/new_patient", json=patient3)
print(r.status_code)
print(r.text)

patient4 = {"patient_id": "4",
            "attending_username": "Ann.A",
            "patient_age": 40}
r = requests.post(hostname + "api/new_patient", json=patient4)
print(r.status_code)
print(r.text)

patient5 = {"patient_id": "5a",
            "attending_username": "Ann.A",
            "patient_age": "a40"}
r = requests.post(hostname + "api/new_patient", json=patient5)
print(r.status_code)
print(r.text)

""" Add heart rate and timestamp """
# Successfully add heart rate and timestamp to patient with strings
hr0 = {"patient_id": "1", "heart_rate": "100"}
r = requests.post(hostname + "api/heart_rate", json=hr0)
print(r.status_code)
print(r.text)

# Check adding additional heart rate to same patient
hr = {"patient_id": "1", "heart_rate": "120"}
r = requests.post(hostname + "api/heart_rate", json=hr)
print(r.status_code)
print(r.text)

# Successfully add heart rate and timestamp to patient with ints
hr1 = {"patient_id": 2, "heart_rate": 110}
r = requests.post(hostname + "api/heart_rate", json=hr1)
print(r.status_code)
print(r.text)

# Check for heart_rate not a dictionary
hr2 = "hello"
r = requests.post(hostname + "api/heart_rate", json=hr2)
print(r.status_code)
print(r.text)

# Check for missing key
hr3 = {"patient_id": "1"}
r = requests.post(hostname + "api/heart_rate", json=hr3)
print(r.status_code)
print(r.text)

# Check for wrong data type
hr4 = {"patient_id": "hello", "heart_rate": 100}
r = requests.post(hostname + "api/heart_rate", json=hr4)
print(r.status_code)
print(r.text)

# Check for missing id
hr5 = {"patient_id": 3, "heart_rate": 130}
r = requests.post(hostname + "api/heart_rate", json=hr5)
print(r.status_code)
print(r.text)

""" Interval Average """
# Check for successful interval average calculation
int_avg1 = {"patient_id": 1, "heart_rate_average_since": "2000-03-09 11:00:36"}
r = requests.post(hostname + "api/heart_rate/interval_average",
                  json=int_avg1)
print(r.status_code)
print(r.text)

# Check for missing id
int_avg2 = {"patient_id": 50,
            "heart_rate_average_since": "2018-03-09 11:00:36"}
r = requests.post(hostname + "api/heart_rate/interval_average",
                  json=int_avg2)
print(r.status_code)
print(r.text)

# Check for future date
int_avg3 = {"patient_id": 1, "heart_rate_average_since": "2100-03-09 11:00:36"}
r = requests.post(hostname + "api/heart_rate/interval_average",
                  json=int_avg3)
print(r.status_code)
print(r.text)

""" All Attending's Patients """
# Check for successful finding of attending's patients
r = requests.get(hostname + "api/patients/Smith.J")
print(r.status_code)
print(r.text)

r = requests.get(hostname + "api/patients/Ann.A")
print(r.status_code)
print(r.text)
