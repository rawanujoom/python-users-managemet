from werkzeug import secure_filename
import os, uuid
from datetime import datetime
from handlers.mariadb_handler import MariaDbHandler
from packages import s3_connector

mariadbHandler = MariaDbHandler()

s3_bucket = 'XYZ'


class ResumeHandler:
    def __init__(self):
        self.media_root = "media"

    def check_admin(self, headers):
        try:
            if headers["X-ADMIN"] == "1":
                return True
            else:
                return False
        except:
            return False

    def post_details(self, data, file):
        try:
            id = str(uuid.uuid4())
            time = datetime.now()

            first_name = data["first_name"].strip()
            last_name = data["last_name"].strip()

            if data["dept_id"] not in ["IT", "HR", "Finance"]:
                response = "Department not allowed"
                return response, 400
            filename = file.filename
            extension = filename.split(".")[-1]
            if extension not in ["docx", "pdf"]:
                response = "File type not allowed"
                return response, 400

            directory = os.path.join(self.media_root, id)
            datapath = os.path.join(directory, secure_filename(filename))
            self.save_to_filesystem(directory, file, datapath)
            # self.save_to_s3(file, s3_bucket, directory)
            datapath = datapath.replace(os.sep, "/")
            query = "INSERT INTO applicants (id,first_name,last_name, dob, years_of_experience, " \
                    "dept_id,path,registration_time) " \
                    "VALUES ('{}','{}','{}', '{}', {} ,'{}','{}','{}');" \
                .format(id, first_name, last_name, data["dob"],
                        data["years_of_experience"], data["dept_id"], datapath, time)
            response = mariadbHandler.insert(query)
            if response:
                return "Submitted successfully", 200
            return "Failed to submit Form", 400
        except Exception as e:
            return "Failed to submit form", 400

    def get_details(self):
        try:
            query = "SELECT * FROM applicants order by registration_time desc;"
            data = mariadbHandler.select(query)
            detailsList = []
            for (id, first_name, last_name, dob, years_of_experience, dept_id, datapath, time) in data:
                details = {"id": id, "first_name": first_name, "last_name": last_name, "dob": dob,
                           "years_of_experience": years_of_experience, "dept_id": dept_id,
                           "path": datapath, "time": str(time)}
                detailsList.append(details)
            return detailsList, 200
        except Exception as e:
            return [], 400

    def get_applicant_resume(self, id):
        try:
            query = "SELECT path FROM applicants where id='{id}';".format(id=id)
            data = mariadbHandler.select(query)
            for each in data:
                fullfilepath = (each[0].replace('/', os.sep))
                filepath = os.sep.join(fullfilepath.split(os.sep)[:-1])
                filename = fullfilepath.split(os.sep)[-1]
                uploads = os.path.join(os.getcwd(), filepath)
                return uploads, filename
            return None, None
        except Exception as e:
            return "Something went wrong", 400

    def save_to_filesystem(self, directory, file, datapath):
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
                file.save(datapath)
                return True
        except Exception as e:
            return False

    def save_to_s3(self, file, bucket, directory):
        status = s3_connector.upload_file(file, bucket, directory)
        return status
