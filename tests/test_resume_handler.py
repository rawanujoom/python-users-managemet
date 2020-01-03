import pytest
from handlers.resume_handler import ResumeHandler
from werkzeug.datastructures import FileStorage
import os, pathlib

resumeHandler = ResumeHandler()


@pytest.fixture
def admin_user():
    headers = {"X-ADMIN": "1"}
    return resumeHandler.check_admin(headers)


@pytest.fixture
def user():
    headers = {}
    return resumeHandler.check_admin(headers)


payload = {
    "first_name": "Rawan",
    "last_name": "N",
    "dob": "2001-09-09",
    "years_of_experience": 3,
    "dept_id": "HR"
}

incorrect_dept_payload = {
    "first_name": "Rawan",
    "last_name": "N",
    "dob": "2001-09-09",
    "years_of_experience": 3,
    "dept_id": "HT"
}

database_entries = 0


def test_initial_get_applicants(admin_user):
    assert admin_user
    global database_entries
    output, status = resumeHandler.get_details()
    database_entries = len(output)
    assert status == 200


def test_correct_payload_docx():
    file = FileStorage(filename="resources/test_dummy.docx")
    output, status = resumeHandler.post_details(payload, file)
    assert output == "Submitted successfully" and status == 200


def test_correct_payload_pdf():
    file = FileStorage(filename="resources/test_dummy.pdf")
    output, status = resumeHandler.post_details(payload, file)
    assert output == "Submitted successfully" and status == 200


def test_incorrect_payload_file():
    file = FileStorage(filename="resources/test_dummy.png")
    output, status = resumeHandler.post_details(payload, file)
    assert output == "File type not allowed" and status == 400


def test_incorrect_deptId_payload():
    file = FileStorage(filename="resources/test_dummy.docx")
    output, status = resumeHandler.post_details(incorrect_dept_payload, file)
    assert output == "Department not allowed" and status == 400


def test_get_applicants(admin_user):
    assert admin_user
    output, status = resumeHandler.get_details()
    final_entries = len(output)
    assert final_entries - database_entries == 2


def test_resume_download(admin_user):
    assert admin_user
    output, status = resumeHandler.get_details()
    id = output[0]["id"]
    uploads, filename = resumeHandler.get_applicant_resume(id)
    if uploads and filename:
        path = os.path.join(uploads, filename)
        file = pathlib.Path(path)
        assert file.exists()
    else:
        assert False


def test_incorrect_resume_download(admin_user):
    assert admin_user
    id = "RANDOM"
    uploads, filename = resumeHandler.get_applicant_resume(id)
    if not uploads and not filename:
        assert True
    else:
        assert False


def test_initial_get_applicants_without_admin_headers(user):
    assert not user
