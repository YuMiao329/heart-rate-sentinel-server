# import pytest
from datetime import datetime
from datetime import timedelta
from testfixtures import LogCapture


def test_parse_new_patient():
    from heart_rate_sentinel import parse_new_patient
    test_parse1 = {"patient_id": 5,
                   "attending_username": "Smith.J",
                   "patient_age": 5}

    test_parse2 = {"patient_id": "5",
                   "attending_username": "Smith.J",
                   "patient_age": "5"}

    test_parse3 = {"patient_id": "5a",
                   "attending_username": "Smith.J",
                   "patient_age": "5"}

    test_parse4 = {"patient_id": "5",
                   "attending_username": "Smith.J",
                   "patient_age": "5a"}

    test_parse5 = {"patient_id": "5",
                   "attending_username": "Smith.J"}

    test_parse6 = {"attending_username": "Smith.J",
                   "patient_age": "5a"}

    expected1 = {"patient_id": 5,
                 "attending_username": "Smith.J",
                 "patient_age": 5}

    expected2 = {"patient_id": 5,
                 "attending_username": "Smith.J",
                 "patient_age": 5}

    expected3 = "Patient ID is not a number or can't convert to integer"

    expected4 = "Patient age is not a number or can't convert to integer"

    expected5 = "No such key: patient_age"

    expected6 = "No such key: patient_id"

    answer1 = parse_new_patient(test_parse1)
    answer2 = parse_new_patient(test_parse2)
    answer3 = parse_new_patient(test_parse3)
    answer4 = parse_new_patient(test_parse4)
    answer5 = parse_new_patient(test_parse5)
    answer6 = parse_new_patient(test_parse6)

    assert answer1 == expected1
    assert answer2 == expected2
    assert answer3 == expected3
    assert answer4 == expected4
    assert answer5 == expected5
    assert answer6 == expected6


def test_validate_new_patient():
    from heart_rate_sentinel import validate_new_patient
    test_in_new_patient1 = {"patient_id": 1,
                            "attending_username": "Smith.J",
                            "patient_age": 50}
    test_in_new_patient2 = {"patient_id": 2,
                            "attending_username": "Ann.A",
                            "patient_age": 40}
    test_in_new_patient3 = {"patient_id": 3,
                            "attending_username": "Ann.A"}
    test_in_new_patient4 = {"patient_id": "4",
                            "attending_username": "Ann.A",
                            "patient_age": 40}
    test_in_new_patient5 = [("patient_id", "5a"),
                            ("attending_username", "Ann.A"),
                            ("patient_age", "a40")]
    test_expected_keys = {"patient_id": int, "attending_username": str,
                          "patient_age": int}
    expected1 = True, 200
    expected2 = True, 200
    expected3 = "The key patient_age is missing from input", 400
    expected4 = True, 200
    expected5 = "The input was not a valid dictionary " \
                "because No dictionary exists", 400

    answer1 = validate_new_patient(test_in_new_patient1,
                                   test_expected_keys)
    answer2 = validate_new_patient(test_in_new_patient2,
                                   test_expected_keys)
    answer3 = validate_new_patient(test_in_new_patient3,
                                   test_expected_keys)
    answer4 = validate_new_patient(test_in_new_patient4,
                                   test_expected_keys)
    answer5 = validate_new_patient(test_in_new_patient5,
                                   test_expected_keys)
    assert answer1 == expected1
    assert answer2 == expected2
    assert answer3 == expected3
    assert answer4 == expected4
    assert answer5 == expected5


def test_add_new_patient():
    from heart_rate_sentinel import add_new_patient
    test_patient_id_1 = 1
    test_attending_username_1 = "Smith.J"
    test_patient_age_1 = 50

    test_patient_id_2 = 2
    test_attending_username_2 = "Ann.A"
    test_patient_age_2 = 50

    expected_1 = {"patient_id": test_patient_id_1,
                  "attending_username": test_attending_username_1,
                  "patient_age": test_patient_age_1}
    answer_1 = add_new_patient(test_patient_id_1,
                               test_attending_username_1,
                               test_patient_age_1)

    expected_2 = {"patient_id": test_patient_id_2,
                  "attending_username": test_attending_username_2,
                  "patient_age": test_patient_age_2}
    answer_2 = add_new_patient(test_patient_id_2,
                               test_attending_username_2,
                               test_patient_age_2)

    assert answer_1 == expected_1
    assert answer_2 == expected_2


def test_validate_new_attending():
    from heart_rate_sentinel import validate_new_attending
    test_in_new_attending1 = {"attending_username": "Smith.J",
                              "attending_email": "dr_user_id@ourdomain.com",
                              "attending_phone": "919-867-5309"}
    test_in_new_attending2 = "attending_username"
    test_in_new_attending3 = {"attending_username": "Smith.J",
                              "attending_email": "dr_user_id@ourdomain.com"}
    test_in_new_attending4 = {"attending_username": 1,
                              "attending_email": "dr_user_id@ourdomain.com",
                              "attending_phone": "919-867-5309"}
    test_expected_keys = {"attending_username": str, "attending_email": str,
                          "attending_phone": str}
    expected1 = True, 200
    expected2 = "The input was not a dictionary", 400
    expected3 = "The key attending_phone is missing from input", 400
    expected4 = "The key attending_username has the wrong data type", 400
    answer1 = validate_new_attending(test_in_new_attending1,
                                     test_expected_keys)
    answer2 = validate_new_attending(test_in_new_attending2,
                                     test_expected_keys)
    answer3 = validate_new_attending(test_in_new_attending3,
                                     test_expected_keys)
    answer4 = validate_new_attending(test_in_new_attending4,
                                     test_expected_keys)
    assert answer1 == expected1
    assert answer2 == expected2
    assert answer3 == expected3
    assert answer4 == expected4


def test_add_new_attending():
    from heart_rate_sentinel import add_new_attending
    test_username = "Smith.J"
    test_email = "dr_user_id@ourdomain.com"
    test_phone = "000-000-0000"
    expected = {"attending_username": test_username,
                "attending_email": test_email,
                "attending_phone": test_phone}
    answer = add_new_attending(test_username, test_email, test_phone)
    assert answer == expected


def test_heart_rate_timestamp():
    pass


def test_validate_heart_rate_timestamp():
    from heart_rate_sentinel import validate_heart_rate_timestamp
    test_in_heart_rate1 = {"patient_id": 1, "heart_rate": 100}
    test_in_heart_rate2 = {"patient_id": "1", "heart_rate": "100"}
    test_in_heart_rate3 = "hello"
    test_in_heart_rate4 = {"patient_id": "1"}
    test_in_heart_rate5 = {"patient_id": "hello", "heart_rate": 100}
    test_expected_keys = {"patient_id": int, "heart_rate": int}
    expected1 = True, 200
    expected2 = True, 200
    expected3 = "The input was not a dictionary", 400
    expected4 = "The key heart_rate is missing from input", 400
    expected5 = "The key patient_id has the wrong data type", 400
    answer1 = validate_heart_rate_timestamp(test_in_heart_rate1,
                                            test_expected_keys)
    answer2 = validate_heart_rate_timestamp(test_in_heart_rate2,
                                            test_expected_keys)
    answer3 = validate_heart_rate_timestamp(test_in_heart_rate3,
                                            test_expected_keys)
    answer4 = validate_heart_rate_timestamp(test_in_heart_rate4,
                                            test_expected_keys)
    answer5 = validate_heart_rate_timestamp(test_in_heart_rate5,
                                            test_expected_keys)
    assert answer1 == expected1
    assert answer2 == expected2
    assert answer3 == expected3
    assert answer4 == expected4
    assert answer5 == expected5


def test_find_patient():
    from heart_rate_sentinel import find_patient
    test_patients_db = [{"patient_id": 1,
                         "attending_username": "Smith.J",
                         "patient_age": 50,
                         "heart_rate": [],
                         "timestamp": []},
                        {"patient_id": 2,
                         "attending_username": "Ann.A",
                         "patient_age": 40}]
    expected1 = {"patient_id": 1,
                 "attending_username": "Smith.J",
                 "patient_age": 50,
                 "heart_rate": [],
                 "timestamp": []}, 0, []
    expected2 = {"patient_id": 2,
                 "attending_username": "Ann.A",
                 "patient_age": 40}, 1, True
    expected3 = {"patient_id": 2,
                 "attending_username": "Ann.A",
                 "patient_age": 40}, 1, False
    answer1 = find_patient(1, test_patients_db)
    answer2 = find_patient(2, test_patients_db)
    answer3 = find_patient(3, test_patients_db)
    assert answer1 == expected1
    assert answer2 == expected2
    assert answer3 == expected3


def test_add_heart_rate_timestamp_keys():
    from heart_rate_sentinel import add_heart_rate_timestamp_keys
    test_id1 = 1
    test_username = "Smith.J"
    test_age = 50
    test_patient = {"patient_id": test_id1,
                    "attending_username": test_username,
                    "patient_age": test_age}
    expected = {"patient_id": test_id1,
                "attending_username": test_username,
                "patient_age": test_age,
                "heart_rate": [],
                "timestamp": []}
    answer = add_heart_rate_timestamp_keys(test_patient)
    assert answer == expected


def test_add_heart_rate_timestamp_info():
    from heart_rate_sentinel import add_heart_rate_timestamp_info
    test_patient1 = {"patient_id": 1,
                     "attending_username": "Smith.J",
                     "patient_age": 50,
                     "heart_rate": [],
                     "timestamp": []}
    test_in_heart_rate = {"patient_id": 1, "heart_rate": 100}
    expected1 = {"patient_id": 1,
                 "attending_username": "Smith.J",
                 "patient_age": 50,
                 "heart_rate": [100],
                 "timestamp": [datetime.now()]}
    answer1 = add_heart_rate_timestamp_info(test_patient1, test_in_heart_rate)
    assert answer1["patient_id"] == expected1["patient_id"]
    assert answer1["attending_username"] == expected1["attending_username"]
    assert answer1["patient_age"] == expected1["patient_age"]
    assert answer1["heart_rate"] == expected1["heart_rate"]
    ans_time_dt1 = datetime.strptime(answer1["timestamp"][0],
                                     "%Y-%m-%d %H:%M:%S")
    exp_time_dt1 = expected1["timestamp"][0]
    assert ans_time_dt1 <= exp_time_dt1 + timedelta(minutes=1)
    test_patient2 = {"patient_id": 1,
                     "attending_username": "Smith.J",
                     "patient_age": 50,
                     "heart_rate": [100],
                     "timestamp": [datetime.now()]}
    expected2 = {"patient_id": 1,
                 "attending_username": "Smith.J",
                 "patient_age": 50,
                 "heart_rate": [100, 100],
                 "timestamp": ["2001-10-10 00:00:00", datetime.now()]}
    answer2 = add_heart_rate_timestamp_info(test_patient2, test_in_heart_rate)
    assert answer2["patient_id"] == expected2["patient_id"]
    assert answer2["attending_username"] == expected2["attending_username"]
    assert answer2["patient_age"] == expected2["patient_age"]
    assert answer2["heart_rate"] == expected2["heart_rate"]
    ans_time_dt2 = datetime.strptime(answer2["timestamp"][-1],
                                     "%Y-%m-%d %H:%M:%S")
    exp_time_dt2 = expected2["timestamp"][-1]
    assert ans_time_dt2 <= exp_time_dt2 + timedelta(minutes=1)


def test_find_patient_all():
    from heart_rate_sentinel import find_patient_all
    test_find_1 = {"patient_id": 1,
                   "attending_username": "Smith.J",
                   "patient_age": 50,
                   "heart_rate": [100]}
    test_find_2 = {"patient_id": 1,
                   "attending_username": "Smith.J",
                   "patient_age": 50,
                   "heart_rate": [120]}
    full_test_list = [test_find_1, test_find_2]
    answer = find_patient_all(1, full_test_list)
    expected = [{"patient_id": 1,
                 "attending_username": "Smith.J",
                 "patient_age": 50,
                 "heart_rate": [100]},
                {"patient_id": 1,
                 "attending_username": "Smith.J",
                 "patient_age": 50,
                 "heart_rate": [120]}
                ]
    assert answer == expected


def test_is_tachy():
    from heart_rate_sentinel import is_tachy
    test_1 = {"patient_id": 1,
              "attending_username": "Smith.J",
              "patient_age": 50,
              "heart_rate": [100]}
    test_2 = {"patient_id": 2,
              "attending_username": "Smith.K",
              "patient_age": 50,
              "heart_rate": [90]}
    answer_1 = is_tachy(test_1)
    answer_2 = is_tachy(test_2)

    expected_1 = "tachycardic"
    expected_2 = "not tachycardic"

    assert answer_1 == expected_1
    assert answer_2 == expected_2


def test_cal_avg_hr():
    from heart_rate_sentinel import cal_avg_hr
    test_1 = [{"patient_id": 1,
               "attending_username": "Smith.J",
               "patient_age": 50,
               "heart_rate": [100]},
              {"patient_id": 1,
               "attending_username": "Smith.J",
               "patient_age": 50,
               "heart_rate": [130]}]

    test_2 = [{"patient_id": 2,
               "attending_username": "Smith.K",
               "patient_age": 50,
               "heart_rate": [120]},
              {"patient_id": 2,
               "attending_username": "Smith.K",
               "patient_age": 50,
               "heart_rate": [130]}]
    answer_1 = cal_avg_hr(test_1)
    answer_2 = cal_avg_hr(test_2)
    expected_1 = 115.0
    expected_2 = 125.0
    assert answer_1 == expected_1
    assert answer_2 == expected_2


def test_interval_average():
    pass


def test_validate_interval_average():
    from heart_rate_sentinel import validate_interval_average
    test1 = {"patient_id": 1,
             "heart_rate_average_since": "2018-03-09 11:00:36"}
    test2 = {"patient_id": "1",
             "heart_rate_average_since": "2018-03-09 11:00:36"}
    test3 = "hello"
    test4 = {"patient_id": 1}
    test5 = {"patient_id": "hello",
             "heart_rate_average_since": "2018-03-09 11:00:36"}
    test_expected_keys = {"patient_id": int, "heart_rate_average_since": str}
    expected1 = True, 200
    expected2 = True, 200
    expected3 = "The input was not a dictionary", 400
    expected4 = "The key heart_rate_average_since is missing from input", 400
    expected5 = "The key patient_id has the wrong data type", 400
    answer1 = validate_interval_average(test1, test_expected_keys)
    answer2 = validate_interval_average(test2, test_expected_keys)
    answer3 = validate_interval_average(test3, test_expected_keys)
    answer4 = validate_interval_average(test4, test_expected_keys)
    answer5 = validate_interval_average(test5, test_expected_keys)
    assert answer1 == expected1
    assert answer2 == expected2
    assert answer3 == expected3
    assert answer4 == expected4
    assert answer5 == expected5


def test_get_patient_hr_entries():
    from heart_rate_sentinel import get_patient_hr_entries
    test1 = {"patient_id": 1,
             "attending_username": "Smith.J",
             "patient_age": 50,
             "heart_rate": [100, 100, 100, 110, 120],
             "timestamp": [datetime(2000, 3, 9, 1, 0, 0),
                           datetime(2000, 3, 9, 2, 0, 0),
                           datetime(2000, 3, 9, 3, 0, 0),
                           datetime(2000, 3, 9, 4, 0, 0),
                           datetime(2000, 3, 9, 12, 0, 0)]}
    expected = [100, 100, 100, 110, 120]
    answer = get_patient_hr_entries(test1)
    assert answer == expected


def test_get_patient_timestamp_entries():
    from heart_rate_sentinel import get_patient_timestamp_entries
    test1 = {"patient_id": 1,
             "attending_username": "Smith.J",
             "patient_age": 50,
             "heart_rate": [100, 100, 100, 110, 120],
             "timestamp": [datetime(2000, 3, 9, 1, 0, 0),
                           datetime(2000, 3, 9, 2, 0, 0),
                           datetime(2000, 3, 9, 3, 0, 0),
                           datetime(2000, 3, 9, 4, 0, 0),
                           datetime(2000, 3, 9, 12, 0, 0)]}
    expected = [datetime(2000, 3, 9, 1, 0, 0),
                datetime(2000, 3, 9, 2, 0, 0),
                datetime(2000, 3, 9, 3, 0, 0),
                datetime(2000, 3, 9, 4, 0, 0),
                datetime(2000, 3, 9, 12, 0, 0)]
    answer = get_patient_timestamp_entries(test1)
    assert answer == expected


def test_calculate_hrs_after():
    from heart_rate_sentinel import calculate_hrs_after
    test_hr_entries = [100, 100, 100, 110, 120]
    test_timestamp_entries = ["2000-03-09 01:00:00",
                              "2000-03-09 02:00:00",
                              "2000-03-09 03:00:00",
                              "2000-03-09 04:00:00",
                              "2000-03-09 12:00:00"]
    test_heart_rate_average_since1 = "2000-03-09 00:00:00"
    test_heart_rate_average_since2 = "2000-03-09 05:00:00"
    test_heart_rate_average_since3 = "2000-03-09 13:00:00"
    test_heart_rate_average_since4 = "2000-04-09 00:00:00"
    expected1 = [100, 100, 100, 110, 120]
    expected2 = [120]
    expected3 = []
    expected4 = []
    answer1 = calculate_hrs_after(test_hr_entries, test_timestamp_entries,
                                  test_heart_rate_average_since1)
    answer2 = calculate_hrs_after(test_hr_entries, test_timestamp_entries,
                                  test_heart_rate_average_since2)
    answer3 = calculate_hrs_after(test_hr_entries, test_timestamp_entries,
                                  test_heart_rate_average_since3)
    answer4 = calculate_hrs_after(test_hr_entries, test_timestamp_entries,
                                  test_heart_rate_average_since4)
    assert answer1 == expected1
    assert answer2 == expected2
    assert answer3 == expected3
    assert answer4 == expected4


def test_calculate_average_since():
    from heart_rate_sentinel import calculate_average_since
    test_hrs_after_time = [100, 100, 100, 110, 120]
    expected = 106
    answer = calculate_average_since(test_hrs_after_time)
    assert answer == expected


def test_attending_patients():
    pass


def test_find_patients():
    from heart_rate_sentinel import find_patients
    test_attending_username1 = "Smith.J"
    test_attending_username2 = "Ann.A"
    test_attending_username3 = "Bob.B"
    test_patients_db = [{"patient_id": 1,
                         "attending_username": "Smith.J",
                         "patient_age": 50,
                         "heart_rate": [100, 100, 100, 110, 120],
                         "timestamp": ["2000-03-09 01:00:00",
                                       "2000-03-09 02:00:00",
                                       "2000-03-09 03:00:00",
                                       "2000-03-09 04:00:00",
                                       "2000-03-09 12:00:00"]},
                        {"patient_id": 2,
                         "attending_username": "Smith.J",
                         "patient_age": 50,
                         "heart_rate": [100, 100, 100, 110, 100],
                         "timestamp": ["2000-03-09 01:00:00",
                                       "2000-03-09 02:00:00",
                                       "2000-03-09 03:00:00",
                                       "2000-03-09 04:00:00",
                                       "2000-03-09 12:00:00"]},
                        {"patient_id": 10,
                         "attending_username": "Bob.B",
                         "patient_age": 100}]
    expected1 = [{"patient_id": 1,
                  "last_heart_rate": 120,
                  "last_time": "2000-03-09 12:00:00",
                  "status": "tachycardic"},
                 {"patient_id": 2,
                  "last_heart_rate": 100,
                  "last_time": "2000-03-09 12:00:00",
                  "status": "tachycardic"}]
    expected2 = []
    expected3 = [{"patient_id": 10,
                  "last_heart_rate": "No entries",
                  "last_time": "No entries",
                  "status": "No entries"}]
    answer1 = find_patients(test_attending_username1, test_patients_db)
    answer2 = find_patients(test_attending_username2, test_patients_db)
    answer3 = find_patients(test_attending_username3, test_patients_db)
    assert answer1 == expected1
    assert answer2 == expected2
    assert answer3 == expected3


def test_validate_attendings_patients():
    from heart_rate_sentinel import validate_attendings_patients
    test_attending_username1 = 1
    test_attending_username2 = "Smith.J"
    test_attending_username3 = "Bob.B"
    test_attending_username4 = "Ann.A"
    test_attending_db = [{"attending_username": "Smith.J",
                          "attending_email": "smith.j@doctor.com",
                          "attending_phone": "000-000-0000"},
                         {"attending_username": "Bob.B",
                          "attending_email": "bob.b@doctor.com",
                          "attending_phone": "000-000-0000"}]
    expected1 = "The input was not a string", 400
    expected2 = True, 200
    expected3 = True, 200
    expected4 = "Attending physician Ann.A not found", 400
    answer1 = validate_attendings_patients(test_attending_username1,
                                           test_attending_db)
    answer2 = validate_attendings_patients(test_attending_username2,
                                           test_attending_db)
    answer3 = validate_attendings_patients(test_attending_username3,
                                           test_attending_db)
    answer4 = validate_attendings_patients(test_attending_username4,
                                           test_attending_db)
    assert answer1 == expected1
    assert answer2 == expected2
    assert answer3 == expected3
    assert answer4 == expected4


def test_get_doc_email():
    from heart_rate_sentinel import get_doc_email
    patient_db = [{'patient_id': 1, 'attending_username': 'Smith.J',
                   'patient_age': 50, 'heart_rate': [100, 120],
                   'timestamp': ['2021-10-29 21:56:53',
                                 '2021-10-29 21:56:53']},
                  {'patient_id': 2, 'attending_username': 'Ann.A',
                   'patient_age': 40, 'heart_rate': [110],
                   'timestamp': ['2021-10-29 21:56:53']},
                  {'patient_id': 4, 'attending_username': 'Ann.A',
                   'patient_age': 40}]
    attending_db = [{'attending_username': 'Smith.J',
                     'attending_email': 'dr_user_id@ourdomain.com',
                     'attending_phone': '919-867-5309'}]
    test_patient_id_1 = 1
    test_heart_rate_1 = [100, 120]
    expected_1 = 'dr_user_id@ourdomain.com'
    answer_1 = get_doc_email(test_patient_id_1, test_heart_rate_1)

    assert expected_1 == answer_1


def test_log_if_new_patient():
    from heart_rate_sentinel import log_if_new_patient
    with LogCapture() as log_c:
        log_if_new_patient(1)
    log_c.check(("root", "INFO", "Added patient id: 1"))
    with LogCapture() as log_c:
        log_if_new_patient(2)
    log_c.check(("root", "INFO", "Added patient id: 2"))
    with LogCapture() as log_c:
        log_if_new_patient(4)
    log_c.check(("root", "INFO", "Added patient id: 4"))


def test_log_if_new_attending():
    from heart_rate_sentinel import log_if_new_attending
    with LogCapture() as log_c:
        log_if_new_attending("Smith.J", "dr_user_id@ourdomain.com")
    log_c.check(("root", "INFO", "Added new attending physician username: "
                                 "Smith.J | email: dr_user_id@ourdomain.com"))
    with LogCapture() as log_c:
        log_if_new_attending("Ann.A", "dr_user_id@ourdomain.com")
    log_c.check(("root", "INFO", "Added new attending physician username: "
                                 "Ann.A | email: dr_user_id@ourdomain.com"))


def test_log_if_no_doc_email():
    from heart_rate_sentinel import log_if_no_doc_email
    with LogCapture() as log_c:
        log_if_no_doc_email()
    log_c.check(("root", "INFO", "No such doctor's email for this patient id"))


def test_log_if_send_email():
    from heart_rate_sentinel import log_if_send_email
    with LogCapture() as log_c:
        log_if_send_email(1, 100, "dr_user_id@ourdomain.com")
    log_c.check(("root", "INFO", "Patient id: 1, heart rate: 100,"
                                 " is tachycardic,the physician"
                                 " email is dr_user_id@ourdomain.com"))
    with LogCapture() as log_c:
        log_if_send_email(1, 120, "dr_user_id@ourdomain.com")
    log_c.check(("root", "INFO", "Patient id: 1, heart rate: 120,"
                                 " is tachycardic,the physician"
                                 " email is dr_user_id@ourdomain.com"))
    with LogCapture() as log_c:
        log_if_send_email(2, 110, "dr_user_id@ourdomain.com")
    log_c.check(("root", "INFO", "Patient id: 2, heart rate: 110,"
                                 " is tachycardic,the physician"
                                 " email is dr_user_id@ourdomain.com"))
