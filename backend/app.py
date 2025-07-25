import logging
from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from auth_utils import authenticate_user 
from make_request_table import get_requests  
from create_task import create_task  # Import the create_task function
import pandas as pd
from get_test_data import get_test_data  # Import the function to get test data   
from is_ended import is_test_ended  # Import the function to check if the test is ended
from get_all_requests import get_all_requests  # Import the function to get all requests
from get_task_detail import get_task_detail  # Import the function to get task detail
from make_test import make_test_data  # Import the function to make test data
from test_copy import test_copy  # Import the function to copy test data
from get_QWK import get_qwk  # Import the function to get QWK data
from get_annotation_data import get_annotation_data
from is_annotation_ended import is_annotation_ended
from make_annotation_data import make_annotation_data


app = Flask(__name__)
CORS(app, origins="https://myapp-frontend-n1ni.onrender.com", supports_credentials=True)
app.logger.setLevel(logging.DEBUG)


TEST_COMPLETION_STATUS = {
    ("3", "2"): False,
}

# def is_test_ended(user_id, task_id):
#     """ユーザーが特定のタスクのテストを完了したかどうかを判定します"""
#     return TEST_COMPLETION_STATUS.get((str(user_id), str(task_id)), False)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Renderのヘルスチェックに応答するためのエンドポイント"""
    return jsonify({"status": "ok"}), 200

@app.route("/api/login", methods=['POST'])
def login_user_():
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
        return make_response(jsonify({"success": False, "message": "無効なユーザー名またはパスワードです","debug":authenticated_user}), 401)

@app.route('/api/all_requests', methods=['POST'])
def get_all_requests_():
    data = request.get_json()
    user_id = str(data.get('user_id'))
    user_tasks = get_all_requests(user_id)
    return make_response(jsonify(user_tasks), 200)

@app.route('/api/task_detail', methods=['POST'])
def get_task_detail_():
    data = request.get_json()
    user_id = str(data.get('user_id'))
    task_id = str(data.get('task_id'))
    task_detail = get_task_detail(user_id, task_id)
    if not task_detail: return jsonify({"success": False, "message": "Task not found"}), 404
    task_detail['test_ended'] = is_test_ended(user_id, task_id)
    return make_response(jsonify(task_detail), 200)

@app.route('/api/get_test_data', methods=['POST'])
def get_test_data_():
    data = request.get_json()
    user_id = str(data.get('user_id'))
    task_id = str(data.get('task_id'))
    answers = get_test_data(user_id, task_id)
    return make_response(jsonify(answers), 200)

@app.route('/api/get_master_test_question', methods=['POST'])
def get_master_test_question():
    data = request.get_json()
    user_id = str(data.get('user_id'))
    task_id = str(data.get('task_id'))
    test_data = get_test_data(user_id, task_id)
    if not test_data: return jsonify({"success": False, "message": "Test data not found"}), 404
    # task_detail = get_test_data(user_id, task_id)
    return make_response(jsonify(test_data), 200)
    # return jsonify({"test_info": test_data, "task_detail": task_detail}), 200

## フロントと形式を相談
@app.route('/api/get_make_data', methods=['POST'])
def make_test_data_():
    data = request.get_json()
    user_id = str(data.get('user_id'))
    task_id = str(data.get('task_id'))
    answers = data.get('answers')
    test_data_id = str(data.get('test_data_id'))
    answer_flg = make_test_data(user_id, test_data_id, answers)
    # if not answer_flg:
    # ここで false になった時のエラー処理はフロント側と相談する
    end = is_test_ended(user_id, task_id)
    return make_response(jsonify({"user_id": user_id, "task_id": task_id, "end": end}), 200)

@app.route('/api/test_copy', methods=['POST'])
def test_copy_():
    data = request.get_json()
    task_id = str(data.get('task_id'))
    user_id = str(data.get('user_id'))
    _, _, success, _ = test_copy(task_id, user_id)
    return make_response(jsonify({"success": success, "user_id": user_id, "task_id": task_id}), 200)

@app.route('/api/get_qwk', methods=['POST'])
def get_qwk_():
    data = request.get_json()
    user_id = str(data.get('user_id'))
    task_id = str(data.get('task_id'))
    qwk_dict = get_qwk(user_id, task_id)
    return make_response(jsonify(qwk_dict["qwk_data"]), 200)

@app.route('/api/get_annotation_data', methods=['POST'])
def get_annotation_data_():
    data = request.get_json()
    user_id = str(data.get('user_id'))
    task_id = str(data.get('task_id'))
    answers = get_annotation_data(user_id, task_id)
    return make_response(jsonify(answers), 200)

@app.route('/api/is_annotation_ended', methods=['POST'])
def is_annotation_ended_():
    data = request.get_json()
    user_id = str(data.get('user_id'))
    task_id = str(data.get('task_id'))
    answers_flg = is_annotation_ended(user_id, task_id)
    return make_response(jsonify({"user_id": user_id, "task_id": task_id, "end": answers_flg}), 200)

# debug queue
@app.route('/api/make_annotation_data', methods=['POST'])
def make_annotation_data_():
    data = request.get_json()
    user_id = str(data.get('user_id'))
    task_id = str(data.get('task_id'))
    annotation_data_id = str(data.get('annotation_data_id'))
    answers = data.get('answers')

    answer_flg = make_annotation_data(user_id, annotation_data_id, answers)
    # if not answer_flg:
    # ここで false になった時のエラー処理はフロント側と相談する
    end = is_annotation_ended(user_id, task_id)
    return make_response(jsonify({"user_id": user_id, "task_id": task_id, "end": end}), 200)


# @app.route('/api/submit_test', methods=['POST'])
# def submit_test():
#     data = request.get_json()
#     user_id = str(data.get('user_id'))
#     task_id = str(data.get('task_id'))
#     answers = data.get('answers')

#     score = 60 
#     passed = score >= 50

#     if passed:
#         TEST_COMPLETION_STATUS[(user_id, task_id)] = True

#     return jsonify({"success": True, "score": score, "passed": passed})




if __name__ == '__main__':
    app.run(debug=True, port=5001)
