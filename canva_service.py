import os
import requests
import json

ACCOUNT_ID = os.environ.get("ACCOUNT_ID")
COURSE_ID = os.environ.get("COURSE_ID")
TOKEN = os.environ.get("TOKEN")


def get_students():
    """
    Get list of students from canvas
    """
    url = f"https://canvas.instructure.com/api/v1/courses/{COURSE_ID}/users"
    headers = {
        'Authorization': f'Bearer {TOKEN}',
        'Content-Type': 'application/json'
    }
    response = requests.request("GET", url, headers=headers)
    return response.json()


def get_last_login_student():
    """
    Get the last login student from canvas
    """
    url = f"https://canvas.instructure.com/api/v1/courses/{COURSE_ID}/users?include_inactive=true&include[]=avatar_url&include[]=enrollments&include[]=email&include[]=observed_users&include[]=can_be_removed&include[]=custom_links"
    headers = {
        'Authorization': f'Bearer {TOKEN}',
        'Content-Type': 'application/json'
    }
    response = requests.request("GET", url, headers=headers)
    students = response.json()

    result = []
    for student in students:
        name = student.get("name")
        short_name = student.get("short_name")
        email = student.get("email")
        role = student["enrollments"][0]["role"]
        last_activity_at = student.get("enrollments")[
            0]["last_activity_at"]
        result.append({
            "name": name,
            "role": role,
            "short_name": short_name,
            "email": email,
            "last_activity_at": last_activity_at
        })
    return result


def invite_user_to_course(email):
    """
    Invite a user
    """
    url = f"https://canvas.instructure.com/api/v1/accounts/{ACCOUNT_ID}/users"
    headers = {
        'Authorization': f'Bearer {TOKEN}',
        'Content-Type': 'multipart/form-data'
    }

    payload = {'pseudonym[unique_id]': email,
               'enrollment[type]': 'StudentEnrollment',
               'user[email]': email,
               'user[terms_of_use]': f"{1}"}

    try:
        response = requests.request(
            "POST", url, headers=headers, data=payload)
        if(response.status_code != 200 and response.status_code != 201):
            raise Exception(response.content)
        return response.json()
    except Exception as e:
        raise e


def enroll_users_to_course(id):
    """
    Enroll users to course
    """
    url = f"https://canvas.instructure.com/api/v1/courses/{COURSE_ID}/enrollments"
    headers = {
        'Authorization': f'Bearer {TOKEN}',
        'Content-Type': 'multipart/form-data;'
    }

    payload = {
        'enrollment[user_id]': id,
        'enrollment[enrollment_state]': 'invited',
        'enrollment[type]': 'StudentEnrollment'
    }

    try:
        response = requests.request(
            "POST", url, headers=headers, data=payload)
        if(response.status_code != 200 and response.status_code != 201):
            raise Exception(response.content)
        return response.json()
    except Exception as e:
        raise e


def create_student(student):
    """
    Create a new student in canvas
    """
    url = f"https://canvas.instructure.com/api/v1/courses/{COURSE_ID}/users"
    headers = {
        'Authorization': f'Bearer {TOKEN}',
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request(
            "POST", url, headers=headers, data=json.dumps(student))
        return response.json()
    except Exception as e:
        return e


'''
student_created = create_student(, student)
print(json.dumps(student_created, indent=2))

students = get_students()
print(json.dumps(students, indent=2))

last_login = get_last_login_student()
print(json.dumps(last_login, indent=2))
'''
