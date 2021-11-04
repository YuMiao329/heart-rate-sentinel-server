![npm](https://img.shields.io/github/followers/YuMiao329?style=flat-square)
![Github Actions Status](https://github.com/BME547-Fall2021/heart-rate-sentinel-server-jimmyu/actions/workflows/pytest_runner.yml/badge.svg)
# Heart Rate Sentinel Server
## By: Jimmy Butch & Yu Miao

The purpose of this repository and program is to run GET and POST requests for a flask server. The information being
sent to and from the server is related to attending physicians, their patients, and various other data entries that
are vital for monitoring their cardiovascular health.
Basically, the server code is responsible for saving inputted information in a database.

## Virtual Environment
#### Please ensure this is done in a virtual environment before installing.
#### A virtual environment can be created by entering 'python -m venv <venv_name>' in the command line.
#### To activate your virtual environment, enter 'source <venv_name>/Scripts/activate' in the command line.
#### All necessary packages can be installed by entering 'pip install -r requirements.txt' in the command line.

## Packages Used:
+ flask
+ datetime
+ logging
+ requests
+ sphinx
+ pytest
+ pycodestyle

## Running the Program
1. First, index to the correct repository 'heart-rate-sentinel-server-jimmyu'
	+ The server can be run locally or on a virtual machine.
2. In either case, enter 'python heart_rate_sentinel.py' on the command line
3. Once the server is on, any of the listed routes can be accessed via a browser window.
	+ Some routes require a json file input.
4. Each json input file must also be saved to the repository folder. (See Server Route Guide for json file formats)
5. If run correctly, the server will output a log file that includes:
	+ Error messages and codes
	+ Patient ID of any newly added patients
	+ Attending username and email for newly added physicians
	+ Patient ID, heart rate, and attending physician's email when a tachycardic heart rate is entered

## Server Route Guide
Server route list and the input/output information for each:
+ /api/new_patient
	+ POST route for new patient information to database
	+ Input json format: {"patient_id": 1,
						  "attending_username": "Smith.J", 
						  "patient_age": 50}
+ /api/new_attending
	+ POST route for new attending physician information to database
	+ Input json format: {"attending_username": "Smith.J",
						  "attending_email": "dr_user_id@yourdomain.com", 
						  "attending_phone": "919-867-5309"}
+ /api/heart_rate
	+ POST route for heart rate information to existing patient
	+ Input json format: {"patient_id": 1,
						  "heart_rate": 100}
+ /api/status/<patient_id>
	+ GET route for most recent heart rate information for a patient
	+ Output json format: {"heart_rate": 100,
						   "status":  "tachycardic" | "not tachycardic",
						   "timestamp": "2018-03-09 11:00:36"}
+ /api/heart_rate/<patient_id>
	+ GET route for all heart rate information for a patient
	+ Output: "heart_rate" (list of integers)
+ /api/heart_rate/average/<patient_id>
	+ GET route to return a patient's overall average heart rate
	+ Output: an average heart rate (single integer)
+ /api/heart_rate/interval_average
	+ POST route for finding the a patient's average heart rate since a designated timestamp
	+ Input json format: {"patient_id": 1,
						  "heart_rate_average_since": "2018-03-09 11:00:36"}
+ /api/patients/<attending_username>
	+ GET route for returning all of an attending physician's patients
	+ Output json format: {"patient_id": 1,
						   "last_heart_rate": 80,
						   "last_time": "2018-03-09 11:00:36",
						   "status":  "tachycardic" | "not tachycardic"}

## Flask API
The Flask API was used to create the server and send and receive information from python.
Flask is a RESTful API that creates "micro-frameworks" for simple web applications.
It has several functions and extensions that were used in this program.
They include:
+ Flask
+ request
+ requests
+ jsonify

## Virtual Machine Hostname

### here is Yu's hostname:
`hostname = "http://vcm-23088.vm.duke.edu:5000/"`
### here is Jimmy's hostname:
`hostname = "http://vcm-23099.vm.duke.edu:5000/"`



## Software License:
This program has an MIT License.
All of the code is open to be edited and distributed.

## Author Information
We are both biomedical engineering Master of Engineering students at Duke University
This repository we created as part of the BME 547 course

## Links
[github repository](https://github.com/BME547-Fall2021/heart-rate-sentinel-server-jimmyu) \
[flask documentation](https://flask.palletsprojects.com/en/2.0.x/) \
[local server](http://127.0.0.1:5000/api/)
