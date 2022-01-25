import os
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

from canva_service import get_last_login_student, enroll_users_to_course, invite_user_to_course

app = Flask(__name__)

cors = CORS(app)


@app.route("/", methods=["GET"])
def index():
    students = get_last_login_student()
    return jsonify(students)


@app.route("/", methods=["POST"])
def new_student():
    email = request.args.get("email")
    try:
        user = invite_user_to_course(email)
        enroll = enroll_users_to_course(user.get("id"))
        return jsonify({
            'user': user,
            'enroll': enroll
        })
    except Exception as e:
        return jsonify({'message': str(e)})


def main():
    port = int(os.environ.get("PORT", 5000))
    app.run(port=port, debug=True)


if __name__ == "__main__":
    main()
