from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from auth_utils import authenticate_user 
from make_request_table import get_requests  
from create_task import create_task  # Import the create_task function
import pandas as pd
# from debag import fetch_all_from_table  # Import the function to fetch data from tables
# from utils.get_ids import get_ids_by_task_id  # Import the function to count questions
# from utils.set_test_data import set_test_data  # Import the function to set test data
# from utils.get_requests import get_questions_by_task  # Import the function to get questions by task ID
# from utils.get_randam_test_id import select_random_unanswered_test  # Import the function to select random unanswered test
# from get_test_data import get_test_data  # Import the function to get test data   
# from make_test import make_test_data  # Import the function to make test data
# from is_ended import is_test_ended  # Import the function to check if the test is ended
# from get_all_requests import get_all_requests  # Import the function to get all requests
# from get_task_detail import get_task_detail  # Import the function to get task detail
# from test_copy import test_copy  # Import the function to copy test data
# from get_qwk import get_qwk  # Import the function to get QWK data

app = Flask(__name__, static_folder="./build/static", template_folder="./build")
CORS(app, origins="http://localhost:5174", supports_credentials=True) #Cross Origin Resource Sharing

@app.route("/", methods=['GET', 'HEAD'])
def home():
    if request.method == 'HEAD':
        return make_response("", 200)  # ← return が必要
    return "Hello, world!", 200


@app.route('/api/login', methods=['POST'])
def login_user():
    data = request.get_json()

    if not data:
        return make_response(jsonify({"success": False, "message": "リクエストボディが空です"}), 400)

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return make_response(jsonify({"success": False, "message": "ユーザー名とパスワードが必要です"}), 400)

    authenticated_user = authenticate_user(username, password)

    if authenticated_user:
        token = "eyJhbGciOiJIUzI1NiIs..." 
        response_data = {
            "success": True,
            "token": token,
            "user": {
                "id": authenticated_user["id"]
            }
        }
        return make_response(jsonify(response_data), 200)
    else:
        return make_response(jsonify({"success": False, "message": "無効なユーザー名またはパスワードです"}), 401)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
