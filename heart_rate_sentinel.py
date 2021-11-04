from flask import Flask, request, jsonify
from datetime import datetime
import logging
import requests

app = Flask(__name__)

# Empty database to add new patients
patients_db = []

# Empty database to add attending physicians
attending_db = []
logging.basicConfig(filename="logfile.log", level=logging.INFO)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


@app.route("/", methods=["GET"])
def status():
    """Used to indicate that the server is running
    """
    return "Server is on"


@app.route("/api", methods=["GET"])
def status_api():
    """Used to indicate that the server/api is running
    """
    return "Server is on"


def parse_new_patient(in_data):
    """To change the input data from string to integer

    This function will take the input data with keys "patient id"
    and "patient age" and change them from string to integer.
    If it contains more than integer it will show an error message.

    :param in_data: JSON contains keys "patient id" and "patient age"
    :return: the changed data format (to int) or error message
    """

    if type(in_data) is not dict:
        return "No dictionary exists"

    if "patient_id" in in_data.keys():
        try:
            in_data["patient_id"] = int(in_data["patient_id"])
        except ValueError:
            return "Patient ID is not a number or can't convert to integer"
    else:
        return "No such key: patient_id"

    if "patient_age" in in_data.keys():
        try:
            in_data["patient_age"] = int(in_data["patient_age"])
        except ValueError:
            return "Patient age is not a number or can't convert to integer"
    else:
        return "No such key: patient_age"

    return in_data


def log_if_new_patient(in_data):
    logging.info("Added patient id: {}".format(in_data))


@app.route("/api/new_patient", methods=["POST"])
def new_patient():
    """Implements /new_patient route for adding a new patient to server
    database
    The /new_patient route is a POST request that should receive a JSON-encoded
    string with the following format:
    {"patient_id": int, "attending_username": str, "patient_age": int}
    The function first calls parse_new_patient to try to change id and age
    to full integer. The function then calls validation functions to ensure
    that the needed keys and data types exist in the received JSON, then
    calls a function to add the patient data to the database.
    The function then returns to the caller either a status code of 200
    and the patient info if it was successfully added, or a status code of
    400 and an error message if there was a validation problem.

    :returns: If the json is in the correct format and data types:
    {"patient_id": int, "attending_username": str, "patient_age": int}
    The JSON file containing patient's information will be
    displayed and stored in database.
    """
    in_data = request.get_json()
    expected_keys = {"patient_id": int,
                     "attending_username": str,
                     "patient_age": int}
    in_data = parse_new_patient(in_data)
    error_string, status_code = validate_new_patient(in_data, expected_keys)
    if error_string is not True:
        return error_string, status_code
    added_patient = add_new_patient(in_data["patient_id"],
                                    in_data["attending_username"],
                                    in_data["patient_age"])
    log_if_new_patient(in_data["patient_id"])
    return "Added patient {}".format(added_patient), 200


def validate_new_patient(in_data, expected_keys):
    """Validates that input data to server contains a dictionary with the
    correct keys and data types
    Various routes for this server are POST requests that receive JSON-encoded
    strings which should contain dictionaries.  To avoid server errors, this
    function checks that the input data is a dictionary, that it has the
    specified keys, and specified data types.
    To specify what the needed keys and data types are, a dictionary is sent
    as a parameter to this function.  The keys of this dictionary are the
    needed keys for the input data and the value for each key is the Python
    data type that should be in the input.  For example:

    {"patient_id": int, "attending_username": str, "patient_age: int}

    :param in_data: The json file that has been read in as a dictionary
    :param expected_keys: A list of the keys needed in the dictionary along
    with their required data types

    :returns: Three possible string error messages that indicate the mistake
    within the inputted json file. This also returns an integer 400 error_code.
    If the json is in the correct format and data types, a True boolean and
    error_code of 200 will be returned as an integer.
    """
    if type(in_data) is not dict:
        return "The input was not a valid dictionary because {}" \
                   .format(parse_new_patient(in_data)), 400
    for key in expected_keys:
        if key not in in_data:
            if key not in in_data:
                return "The key {} is missing from input".format(key), 400
            if type(in_data[key]) is not expected_keys[key]:
                return "The key {} has the wrong data type".format(key), 400
    return True, 200


def add_new_patient(patient_id, attending_username, patient_age):
    """Creates new patient database entry
    This function receives information about the patient,
    creates a dictionary, and appends that dictionary to the database list.
    The patient dictionary has the following format:
    {"patient_id": str, "attending_username": int, "patient_age": str,
     "tests": list}
    The "tests" list is initialized as an empty list while the values for the
    other keys are taken from the input parameters.  After the new patient
    is added, the database is printed to the console for debugging purposes.
    The created dictionary is returned to enable this function to be tested.
    This function takes the information from each of the expected_keys and
    adds it to the attending physician database as a dictionary.

    :param patient_id: A string of the new patient id
    :param attending_username: A string of the new attending physician's
    username
    :param patient_age: A string of the new patient age

    :returns: Returns the four parameters in a dictionary format under the
    keys: "patient_id", "attending_username", "patient_age", and "tests"
    """
    patient_to_add = {"patient_id": patient_id,
                      "attending_username": attending_username,
                      "patient_age": patient_age}
    patients_db.append(patient_to_add)
    print(patients_db)
    return patient_to_add


def log_if_new_attending(attending_username, attending_email):
    logging.info("Added new attending physician username: {} | "
                 "email: {}".format(attending_username,
                                    attending_email))


@app.route("/api/new_attending", methods=["POST"])
def new_attending():
    """ Driver function for validating and adding new attending physicians

    This function has two parts. The first part reads an inputted json file
    and validates then runs it through the validation function.
    The returns from validate_new_attending pass, then the inputted information
    is sent to the the in_new_attending function to add the attending physician
    to the database. This information includes their username, email, and phone
    number. Once added to the database, the return message will indicate that a
    new physician has been added along with their username and phone.

    :returns: A message that reads "Added new attending physician <username> |
    <phone number>"
    """
    in_new_attending = request.get_json()
    expected_keys = {"attending_username": str, "attending_email": str,
                     "attending_phone": str}
    error_string, status_code = validate_new_attending(in_new_attending,
                                                       expected_keys)
    if error_string is not True:
        return error_string, status_code
    added_attending = add_new_attending(in_new_attending["attending_username"],
                                        in_new_attending["attending_email"],
                                        in_new_attending["attending_phone"])
    log_if_new_attending(added_attending["attending_username"],
                         added_attending["attending_email"])
    return "Added new attending physician {} | {}".format(
        added_attending["attending_username"],
        added_attending["attending_phone"]), 200


def validate_new_attending(in_new_attending, expected_keys):
    """ Validates inputted json data

    This function tests 3 criteria for the inputted json file.
    1. It must be a dictionary
    2. It must contain all of the expected_keys: "attending_username",
       "attending_email", and "attending_phone"
    3. It must contain the correct data types for each key. All values must be
       strings.
   The appropriate error message will be returned based on what the json file
   is missing or has incorrect.
   If the json file has the correct format and data types, the function will
   return True, 200 as a passing boolean and status_code.

   :param in_new_attending: The json file that has been read in as a dictionary
   :param expected_keys: A list of the keys needed in the dictionary along with
   their required data types

   :returns: Three possible string error messages that indicate the mistake
   within the inputted json file. This also returns an integer 400 error_code.
   If the json is in the correct format and data types, a True boolean and
   error_code of 200 will be returned as an integer.
   """
    if type(in_new_attending) is not dict:
        return "The input was not a dictionary", 400
    for key in expected_keys:
        if key not in in_new_attending:
            return "The key {} is missing from input".format(key), 400
        if type(in_new_attending[key]) is not expected_keys[key]:
            return "The key {} has the wrong data type".format(key), 400
    return True, 200


def add_new_attending(username, email, phone):
    """ Add new attending physician information to database

    This function takes the information from each of the expected_keys and
    adds it to the attending physician database as a dictionary.

    :param username: A string of the new attending physician's username
    :param email: A string of the new attending physician's email
    :param phone: A string of the new atteding physician's phone number

    :returns: Returns the three parameters in a dictionary format under the
    keys: "attending_username", "attending_email", and "attending_phone"
    """
    attending_to_add = {"attending_username": username,
                        "attending_email": email,
                        "attending_phone": phone}
    attending_db.append(attending_to_add)
    print(attending_db)
    return attending_to_add


@app.route("/api/heart_rate", methods=["POST"])
def heart_rate_timestamp():
    """ Implements /api/heart_rate route

    This function is a driver for the validate_heart_rate, find_patient,
    add_heart_rate_timestamp_keys, add_heart_rate_timestamp_info, and
    add_hr_to_db functions.
    It first reads in a json file in the correct format that contains a
    patient_id and a heart_rate reading.
    The inputted data is validated and can return True, 200 if no errors
    occurred or it can return an error string and a 400 error code. The error
    string describes the error that occurred with the inputted json file.
    The find_patient will then run the find_patient function and return the
    patient information, an indexing location ("enum"), and a status. The
    status can be False, True, or []. If False, the patient was not found in
    the database and an appropriate error message will be returned.
    If True, this means that the patient is receiving their first heart_rate
    and timestamp entry. This will then run the add_heart_rate_timestamp
    function.
    If status = [], then the program will skip to the
    add_heart_rate_timestamp_info function and append the new information.
    Finally, the new information and created patient dictionary will be added
    to the patients_db using the add_hr_to_db function.

    :returns: If the status_code from validate_heart_rate_timestamp is 400, an
    error string and the error code will be returned describing the error.
    If the entered patient ID is not found in the database, a 400 error code
    and error string will be returned.
    If status from find_patient is False, an error message will be returned
    indicating the missing Patient ID.
    If the patient ID is found and there are no validation errors, the function
    will return "Added test to patient id <patient_id>", 200
    """
    in_heart_rate = request.get_json()
    heart_rate_expected_keys = {"patient_id": int, "heart_rate": int}
    error_string, status_code = \
        validate_heart_rate_timestamp(in_heart_rate, heart_rate_expected_keys)
    if error_string is not True:
        return error_string, status_code
    patient, enum, status = find_patient(in_heart_rate["patient_id"],
                                         patients_db)
    if status is False:
        return "Patient ID {} not found in database" \
                   .format(in_heart_rate["patient_id"]), 400
    if status is True:
        patient = add_heart_rate_timestamp_keys(patient)
    new_entry = add_heart_rate_timestamp_info(patient, in_heart_rate)
    send_email(new_entry["patient_id"], new_entry["heart_rate"][-1])
    add_hr_to_db(patients_db, enum, new_entry)
    print("here is the dbdbdbdb")
    print(patients_db)
    return "Added test to patient id " \
           "{}".format(in_heart_rate["patient_id"]), 200


def add_hr_to_db(patients_db, enum, new_entry):
    """ Replace old patient information with new information

    This function is responsible for taking the old patient dictionary and
    replacing it with a new patient dictionary. This new dictionary contains
    any new heart rate and timestamp information that has been added on the
    /api/heart_rate route.

    :param patients_db: a list of dictionaries. Each dictionary contains
    information for each patient. Format:
        {'patient_id': 1,
         'attending_username': 'Smith.J',
         'patient_age': 50,
         'heart_rate': [],
         'timestamp': []}
    :param enum: an integer that is used to index the location of the new
    patient dictionary in the patients_db
    :param new_entry: the new patient dictionary that will replace the old
    dictionary in the patients_db. Format:
        {'patient_id': 1,
         'attending_username': 'Smith.J',
         'patient_age': 50,
         'heart_rate': [100,...],
         'timestamp': ["2018-11-02 11:00:00,..."]}

    :returns: the new patients_db with the updated patient dictionary (shown
    above)
    """
    patients_db[enum] = new_entry
    return patients_db


def validate_heart_rate_timestamp(in_heart_rate, heart_rate_expected_keys):
    """Validate inputted json data

    This function tests 3 criteria for the inputted json file.
    1. It must be a dictionary
    2. It must contain all of the expected_keys: "patient_id" and
    "heart_rate"
    3. It must contain the correct data types for each key. All values must be
       integers or integers in a string format.
   The appropriate error message will be returned based on what the json file
   is missing or has incorrect.
   If the json file has the correct format and data types, the function will
   return True, 200 as a passing boolean and status_code.
   This function will also validate any integers that have been entered as a
   string data type.

   :param in_heart_rate: This is a dictionary from the inputted json file
   :param heart_rate_expected_keys: This is a dictionary containing keys for
   "patient_id" and "heart_rate". The value of each key is the expected data
   type (int).

   :returns: This function returns either an error string and an error code
   describing the validation error, or True, 200 if no errors occurred.
   """
    if type(in_heart_rate) is not dict:
        return "The input was not a dictionary", 400
    for key in heart_rate_expected_keys:
        if key not in in_heart_rate:
            return "The key {} is missing from input".format(key), 400
        if type(in_heart_rate[key]) is not heart_rate_expected_keys[key]:
            try:
                in_heart_rate[key] = int(in_heart_rate[key])
            except ValueError:
                return "The key {} has the wrong data type".format(key), 400
    return True, 200


def find_patient(patient_id, patients_db):
    """Find patient dictionary from database

    This function pulls the patients dictionary based on the patient_id entered
    in the json file. If the entered patient_id is not found in the patient
    database, then a False "status" boolean is returned. This output is used in
    the heart_rate_timestamp function.
    This function also returns the patient dictionary, if found, and the enum
    variable. "Enum" is used to count the number of iterations through the
    for loop in the function. This allows us to locate the index for the
    specified patient in the patients database.

    :param patient_id: The patient_id number from the inputted json as an
    integer
    :param patients_db: The master database containing dictionaries for each
    entered patient

    :returns: This function will return "patient" which is a dictionary
    corresponding to the entered patient_id number.
    It can return False as a boolean if the entered patient_id number is not
    found in the database.
    Enum is an integer returned as an indexing tool in later functions.
    The third return is a "status" that can be [], True, or False.
    """
    for enum, patient in enumerate(patients_db):
        if patient["patient_id"] == patient_id:
            for key in {"timestamp": [], "heart_rate": []}:
                if key in patient:
                    return patient, enum, []
                else:
                    return patient, enum, True
    return patient, enum, False


def add_heart_rate_timestamp_keys(patient):
    """ Add empty keys for heart_rate and timestamps

    This function adds an empty list to the patient's dictionary information.
    This is a preliminary step so that heart_rate and timestamp information can
    later be added to the server in the heart_rate_timestamp function.
    Note: this function only runs if there are no heart_rate and timestamp
    entries in the past.

    :param patient: A dictionary conataining information in the format:
        {"patient_id": patient_id,
         "attending_username": attending_username,
         "patient_age": patient_age}
add
    :returns: A dictionary with added empty lists for the "heart_rate" and
    "timestamp" keys. The first three keys are "patient_id",
    "attending_username", and "patient_age".
    """
    patient_id = patient["patient_id"]
    attending_username = patient["attending_username"]
    patient_age = patient["patient_age"]
    patient_new_keys = {"patient_id": patient_id,
                        "attending_username": attending_username,
                        "patient_age": patient_age,
                        "heart_rate": [],
                        "timestamp": []}
    return patient_new_keys


def add_heart_rate_timestamp_info(patient_new_keys, in_heart_rate):
    """ Add heart_rate and timestamp to patient dictionary

    This function appends the information to the dictionary of an entered
    patient. The information being added is the "heart_rate" and "timestamp"
    for the heart_rate reading. This function is used within the
    heart_rate_timestamp function to add the heart_rate and timestamp
    information to the patient database and server.

    :param patient: A dictionary in the format:
        {"patient_id": patient_id,
         "attending_username": attending_username,
         "patient_age": patient_age,
         "heart_rate": [],
         "timestamp": []}
    :param in_heart_rate: A dictionary that contains "patient_id" and
    "heart_rate" values as integers.

    :returns: An updated dictionary for the entered patient ID with their
    heart rate reading and a timestamp for the reading. Ex:
        {"patient_id": patient_id,
         "attending_username": attending_username,
         "patient_age": patient_age,
         "heart_rate": 100,
         "timestamp": "2018-03-09 11:00:36"}
    """
    heart_rate_to_add = in_heart_rate["heart_rate"]
    patient_new_keys["heart_rate"].append(heart_rate_to_add)
    timestamp_to_add = datetime.now()
    timestamp_to_add = datetime.strftime(timestamp_to_add, "%Y-%m-%d %H:%M:%S")
    patient_new_keys["timestamp"].append(timestamp_to_add)
    return patient_new_keys


def find_patient_all(patient_id, patients_db):
    """Find all data for one patient from database

    This function pulls the patients' all dictionary based on the
    patient_id entered in the json file. If the entered patient_id is
    not found in the patient database, then a False boolean is returned.
    This output is used in the heart_rate_timestamp function.

    :param patient_id: The patient_id number from the inputted json as an
    integer
    :param patients_db: The master database containing dictionaries for each
    entered patient

    :returns: This function will return a list of all data from one specific
    patient id corresponding to the entered patient_id number.
    """
    find_all_list = []
    for patient in patients_db:
        if patient["patient_id"] == patient_id:
            for key in {"timestamp": [], "heart_rate": []}:
                if key in patient:
                    find_all_list.append(patient)
                    break
    return find_all_list


def is_tachy(patient):
    """Calculate if this patient has tachycardia or not based
    on the valu of heart rate

    If heart rate is larger than 100, it will return "tachycardic",
    otherwise, it will return "not tachycardic"

    :param patient: The data of a patient in JSON

    :returns: If heart rate is larger than 100, it will return "tachycardic",
    otherwise, it will return "not tachycardic"
    """
    if patient["heart_rate"][-1] >= 100:
        return "tachycardic"
    else:
        return "not tachycardic"


def cal_avg_hr(find_all_list):
    """Calculate the average heart rate given multiple of data
    registered from client

    It wil collect multiple data from different time stamp and
    return the average value.

    :param find_all_list: The list of data of a patient in JSON

    :returns: The average heart beat value of a list: find_all_list
    """
    avg_hr = 0
    count = 0
    for patient in find_all_list:
        avg_hr += patient["heart_rate"][-1]
        count += 1
    return avg_hr / count


@app.route("/api/status/<patient_id>", methods=["GET"])
def check_status_by_id(patient_id):
    """Create a JSON file containing the most recent time stamp,
    heart rate and status of the patient id

    It wil collect multiple data from different time stamp and
    select the latest one and use is_tachy function to get the
    status of the patient. Then it returns all other items in
    the same JSON file.

    :param patient_id: The id of the patient

    :returns: The JSON file containing heart rate,
    status and time stamp. If there is no such patient, it will
    return "No patient's information" or "No timestamp or
    heart_Rate data available for this patient id"
    """
    patient = find_patient_all(int(patient_id), patients_db)
    print("find find patient all:")
    print(patients_db)
    # return jsonify(patient)
    try:
        patient = patient[-1]
        print("look here")
        print(patient)
        status = is_tachy(patient)
        print(status)
        timestamp = patient["timestamp"]
        heart_Rate = patient["heart_rate"]
        status_json = {"heart_rate": heart_Rate,
                       "status": status,
                       "timestamp": timestamp}
        if status == "tachycardic":
            if not get_doc_email(patient_id, heart_Rate):
                return "No such doctor's email", 400
        return status_json, 200
    except TypeError:
        return "No patient's information", 400
    except IndexError:
        return "No timestamp or heart_Rate" \
               " data available for this patient id", 400


def log_if_no_doc_email():
    logging.info("No such doctor's email for this patient id")


def get_doc_email(patient_id, heart_Rate):
    """Return the doctor's email for the patient id

    It will get the patient id from the argument and find
    the corresponding attending doctor's username fro the
    patient data base and then query from the attending
    doctor's database to find the corresponding email

    :param patient_id: The id of the patient
    :param heart_Rate: The heart rate array of the patient

    :returns: the doctor's email based on the patient id.
    Will return False if there is no doctors email for this
    patient id.
    """
    try:
        for patient in patients_db:
            if int(patient_id) == patient["patient_id"]:
                doc_name = patient["attending_username"]
                for doc in attending_db:
                    if doc["attending_username"] == doc_name:
                        doc_email = doc["attending_email"]

                        return doc_email
    except KeyError:
        log_if_no_doc_email()
        return False


def log_if_send_email(patient_id, heart_Rate, doc_email):
    logging.info("Patient id: {}, heart rate: {}, is tachycardic,"
                 "the physician email is {}"
                 .format(patient_id, heart_Rate, doc_email))


def send_email(patient_id, heart_Rate):
    """Send the email through server:
     "http://vcm-7631.vm.duke.edu:5007/hrss/send_email"

    If the patient has tachycardic based on his/her recent record
    of heart rate, it will send a email to the doctor's email.

    :param patient_id: The id of the patient
    :param heart_Rate: The heart rate array of the patient

    :returns: The text string showing that
    "E-mail sent to dr_user_id@ourdomain.com from server@domain.com"
    with code returned. 200 if pass. 400 if not pass.

    """
    doc_email = get_doc_email(patient_id, heart_Rate)
    email = {
        "from_email": "server@domain.com",
        "to_email": doc_email,
        "subject": "Tachycardic!",
        "content": "Patient {} has a tachycardic heart rate!"
        .format(patient_id)
    }
    log_if_send_email(patient_id, heart_Rate, doc_email)
    r = requests.post("http://vcm-7631.vm.duke.edu:5007/hrss/send_email",
                      json=email)
    print(r.status_code)
    print(r.text)
    return r.text, r.status_code


@app.route("/api/heart_rate/<patient_id>", methods=["GET"])
def check_hr_by_id(patient_id):
    """Return the list of heart beat of this patient from all
    his/her records existed

    It will get all data from this particular patient's id and
    get all dictionary with heart rate. Finally, return all
    heart rate in the list

    :param patient_id: The id of the patient

    :returns: List of all heart rate recorded for this patient id
    or "No heart rate data available" is there is no "heart_rate"
    for the patient id
    """
    patient = find_patient_all(int(patient_id), patients_db)
    list_hr = []
    try:
        for record in patient:
            list_hr.append(record["heart_rate"][-1])
        return jsonify(list_hr), 200
    except KeyError:
        return "No heart rate data available", 400


@app.route("/api/heart_rate/average/<patient_id>", methods=["GET"])
def check_avghr_by_id(patient_id):
    """Return the average heart rate based on the list of heart
    rate available

    It will receive the full data of a patient and use function
    cal_avg_hr to calculate the average value

    :param patient_id: The id of the patient

    :returns: The average heart rate from the patient id, or
    "No average heart rate data available" if there is no heart rate
    key in the dictionary
    """
    find_all_list = find_patient_all(int(patient_id), patients_db)
    avg_hr = cal_avg_hr(find_all_list)
    try:
        return jsonify(avg_hr), 200
    except KeyError:
        return "No average heart rate data available", 400


@app.route("/api/heart_rate/interval_average", methods=["POST"])
def interval_average():
    """ POST server route to add avearge heart rate since a specified date

    This function first reads in a json file in the format:
        {"patient_id": 1,
         "heart_rate_average_since": "2018-03-09 11:00:36"}

    It is the driver code for the validate_interval_average,
    get_patient_hr_entries, get_patient_timestamp_entries, calculate_hrs_after,
    and calulate_average_since functions. Each of these functions are explained
    in later docstrings.
    interval_average will return error strings and status codes based on
    errors within the program. Each error string describes the error and a 400
    error code indicates an error, while a 200 error code indicates no error.
    Errors include, no patient_id found and entering a future date.
    If the correctly formatted data is entered, the program will return a
    string indicating the entered date and the patient's average heart rate
    since that date.

    :returns: Returns error strings and status codes based on
    errors within the program. Each error string describes the error and a 400
    error code indicates an error, while a 200 error code indicates no error.
    Errors include, no patient_id found and entering a future date.
    If the correctly formatted data is entered, the program will return a
    string indicating the entered date and the patient's average heart rate
    since that date.
    """
    in_int_avg = request.get_json()
    expected_keys = {"patient_id": int, "heart_rate_average_since": str}
    error_string, status_code = validate_interval_average(in_int_avg,
                                                          expected_keys)
    if error_string is not True:
        return error_string, status_code

    patient, enum, status = find_patient(in_int_avg["patient_id"], patients_db)
    if status is False:
        return "Patient ID {} not found in database" \
                   .format(in_int_avg["patient_id"]), 400
    if status is True:
        return "Patient does not have heart_rate information", 400
    all_hr_entries = get_patient_hr_entries(patient)
    all_timestamps = get_patient_timestamp_entries(patient)
    hrs_after_time = \
        calculate_hrs_after(all_hr_entries, all_timestamps,
                            in_int_avg["heart_rate_average_since"])
    if len(hrs_after_time) == 0:
        return "{} is a future date, no data found" \
                   .format(in_int_avg["heart_rate_average_since"]), 400
    average_since = calculate_average_since(hrs_after_time)
    return "Average heart rate since {} is {}".format(
        in_int_avg["heart_rate_average_since"],
        int(average_since)), 200


def validate_interval_average(in_int_avg, expected_keys):
    """ Validates entered data for interval_average function

    This function tests 3 criteria for the inputted json file.
    1. It must be a dictionary
    2. It must contain all of the expected_keys: "patient_id" and
    "heart_rate"
    3. It must contain the correct data types for each key. Patient ID
    values must be integers or integers in a string format.
   The appropriate error message will be returned based on what the json file
   is missing or has incorrect.
   If the json file has the correct format and data types, the function will
   return True, 200 as a passing boolean and status_code.
   This function will also validate any integers that have been entered as a
   string data type.
    :param in_int_avg: a dictionary containing the information from the input
    json file
    :param expected_keys: a dictionary containing the expected data types of
    each key in the json file

    :returns: Error strings and codes (400) will be returned if one of the 3
    criteria above is broken. Each error string indicates a unique error.
    If no errors occur, the program will return an error string that is True
    and a 200 error code.
    """
    if type(in_int_avg) is not dict:
        return "The input was not a dictionary", 400
    for key in expected_keys:
        if key not in in_int_avg:
            return "The key {} is missing from input".format(key), 400
        if type(in_int_avg[key]) is not expected_keys[key]:
            try:
                in_int_avg[key] = int(in_int_avg[key])
            except ValueError:
                return "The key {} has the wrong data type".format(key), 400
    return True, 200


def get_patient_hr_entries(patient):
    """ Get heart rate information from patient database

    This function indexes the patient database dictionary and pulls all heart
    rate entries. The entries are then saved in the "all_hr_entries" variable.

    :param patient: A dictionary containing all of a patient's information

    :returns: a list of all of the indicated patient's heart rate entries
    """
    all_hr_entries = patient["heart_rate"]
    return all_hr_entries


def get_patient_timestamp_entries(patient):
    """ Get timestamp information from patient database

    This function indexes the patient database dictionary and pulls each
    timestamp for each heart rate entry. The entries are then saved in the
    "all_timestampes" variable.

    :param patient: A dictionary containing all of a patient's information

    :returns: a list of all of the indicated patient's heart rate entry
    timestamps
    """
    all_timestamps = patient["timestamp"]
    return all_timestamps


def calculate_hrs_after(all_hr_entries, all_timestamps,
                        heart_rate_average_since):
    """ Find heart rate entries after indicated time

    This function uses a for loop and if/else statement to index and make a
    list of all the heart rate entries that occur after the
    "heart_rate_average_since" date (from inputted json).
    If the date is a future date, an empty list will be returned.

    :param all_hr_entries: a list of all the indicated patient's heart rate
    entries
    :param all_timestamps: a list of all the indicated patient's heart rate
    entry timestamps
    :param heart_rate_average_since: a string containing the desired date. All
    heart rates entered after this date will be averaged.

    :returns: A list of heart rate values that were entered after the indicated
    date. An empty list will be returned if the date is in the future.
    """
    average_since = datetime.strptime(heart_rate_average_since,
                                      "%Y-%m-%d %H:%M:%S")
    hrs_after_time = []
    for entry in range(0, len(all_hr_entries)):
        if datetime.strptime(all_timestamps[entry], "%Y-%m-%d %H:%M:%S") \
                > average_since:
            hrs_after_time.append(all_hr_entries[entry])
    return hrs_after_time


def calculate_average_since(hrs_after_time):
    """ Calculate average heart rate after specified date

    This function first sums all of the heart rates after the specified date.
    It then divides the summed heart rates by the total number of heart rate
    entries. The result is the sum of the heart rates after the entered time.

    :param hrs_after_time: a list of heart rate values that were entered after
    the specified time ("heart_rate_average_since")

    :returns: an integer indicating the average heart rate of the patient after
    a certain date
    """
    total_entries = len(hrs_after_time)
    average_since = sum(hrs_after_time) / total_entries
    return average_since


@app.route("/api/patients/<attending_username>", methods=["GET"])
def attendings_patients(attending_username):
    """ Server route to GET a single physicians patients

    This function is a driver for the find_patients and
    validate_attendings_patients functions. Its purpose is to pull information
    from the server/patient and attending databases. The information that it
    pulls is a list of patient dictionaries named "all_patients_list."
    Each dictionary in the list contains information for each of the
    attending user's patients. The attending user is specified by their
    <attending_username> entered in the URL.

    :param attending_username: a string containing the attending physician's
    username. (saved from URL)

    :returns: 1. a list of patient information dictionaries. This is also the
    return of the find_patients function. This may also be an empty list if
    the attending physician exists in the database, but does not have any
    assigned patients.
        2. an error string and error code indicating an error with the entered
        attending_username. An error will be returned if the username is not a
        string data type. An error will also be returned if the username does
        not exist in the database. True, 200 will be returned if no errors
        occur.
    """
    print("Searching for {}...".format(attending_username))
    error_string, error_code = validate_attendings_patients(attending_username,
                                                            attending_db)
    print("Attending DB:")
    print(attending_db)
    if error_string is not True:
        return error_string, error_code
    all_patients_list = find_patients(attending_username, patients_db)
    print("{}'s patients:".format(attending_username))
    print(all_patients_list)
    return jsonify(all_patients_list), 200


def find_patients(attending_username, patients_db):
    """ Find all patients for a single physician

    This function searches the patient database for all patients that are being
    treated by a single physician. If a patient's attending physician matches
    the "attending_username" parameter, their dictionary will be added to a
    list of that physicians patients. Each dictionary is in the format:
    Example:   {"patient_id": 1,
                "last_heart_rate": 100,
                "last_time": "2018-03-09 11:00:00",
                "status": "tachycardic"}

    :param attending_username: a string containing the attending physician's
    username (from URL)
    :param patients_db: a list of patient dictionaries containing the
    information from each patient entered in the database

    :returns: a list of dictionaries for patients that are being treated by
    the specified attending physician. This may also return an empty list ([])
    if the physician is not treating any patients currently.
    """
    all_patients_list = []
    for patient in patients_db:
        if patient["attending_username"] == attending_username:
            for key in {"timestamp": [], "heart_rate": []}:
                if key in patient:
                    dictionary = {"patient_id": patient["patient_id"],
                                  "last_heart_rate":
                                      int(patient["heart_rate"][-1]),
                                  "last_time": patient["timestamp"][-1],
                                  "status": is_tachy(patient)}
                else:
                    dictionary = {"patient_id": patient["patient_id"],
                                  "last_heart_rate": "No entries",
                                  "last_time": "No entries",
                                  "status": "No entries"}
            all_patients_list.append(dictionary)
    return all_patients_list


def validate_attendings_patients(attending_username, attending_db):
    """  Validate inputted attending_username

    This function is a check to see if the attending_username (inputted from
    the URL) is in the proper format or exists in the database. If the entered
    attending_username is not a string data type, the function will return
    an error describing this and a 400 error code.
    If the attending_username is not found in the database, the function will
    return an error describing this and a 400 error code.
    If the attending_username does exist in the database, True, 200 will be
    returned as a passing error string and error code.

    :param attending_username: a string containing the attending physician's
    username (from URL)
    :param attending_db: a list of attending physician dictionaries containing
    the information from each attending physician entered in the database.

    :returns: An error string and error code in the format:
    error_string, error_code
    1. If the attending_username was not a string, the function will
    return: "The input was not a string", 400.
    2. If the attending_username was found in the databse, the function will
    return: True, 200
    3. If the attending_username was not found, the function will return:
        "Attending physician <attending_username> not found", 400.
    """
    if type(attending_username) is not str:
        return "The input was not a string", 400
    for physician in attending_db:
        if physician["attending_username"] == attending_username:
            return True, 200
    return "Attending physician {} not found".format(attending_username), 400


if __name__ == "__main__":
    app.run()
