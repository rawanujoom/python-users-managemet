# python-users-managemet

## Setup
* Create a virtual environment virtualenv -p python3 venv

* source venv/bin/activate

* Install packages: pip install -r requirements.txt

* Run prerequisites: python prerequisites.py

* Run Flask server: python main.py


## Endpoints:
1. /resume/

    GET (requires admin Headers)

    POST : Resumes can be saved in to S3 using save_to_s3 uncomment that and comment save_to_filesystem usage.

2. /resume/download/<ID>

    GET (requires admin Headers)


### Admin Headers:
X-Admin = 1

### Request Payload:
POST: 
/resume/ 

Keys:
first_name, last_name, dob, years_of_experience, dept_id, file

