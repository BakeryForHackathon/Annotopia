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
from utils.get_requests import get_questions_by_task  # Import the function to get questions by task ID
from make_test import make_test_data  # Import the function to make test data

# from debag import fetch_all_from_table  # Import the function to fetch data from tables
# from utils.get_ids import get_ids_by_task_id  # Import the function to count questions
# from utils.set_test_data import set_test_data  # Import the function to set test data
# from utils.get_randam_test_id import select_random_unanswered_test  # Import the function to select random unanswered test
# from test_copy import test_copy  # Import the function to copy test data
# from get_qwk import get_qwk  # Import the function to get QWK data


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

##### 
@app.route('/api/submit_test_answer', methods=['POST'])
def submit_test_answer():
    data = request.get_json()
    user_id, task_id = str(data.get('user_id')), str(data.get('task_id'))
    answer = data.get('answer')
    key = (user_id, task_id)
    if key not in USER_TEST_ANSWERS: USER_TEST_ANSWERS[key] = []
    USER_TEST_ANSWERS[key].append(answer)
    total_questions = DUMMY_TEST_DATA.get(task_id, {}).get("total_questions", 0)
    if len(USER_TEST_ANSWERS[key]) >= total_questions:
        score = 60
        passed = score >= 50
        if passed: TEST_COMPLETION_STATUS[key] = True
        del USER_TEST_ANSWERS[key]
        return jsonify({"success": True, "end": True, "result": {"score": score, "passed": passed}})
    return jsonify({"success": True, "end": False})

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

@app.route('/api/make_test_data', methods=['POST'])
def make_test_data_():
    data = request.get_json()
    user_id = str(data.get('user_id'))
    task_id = str(data.get('task_id'))
    test_data_id = str(data.get('test_data_id'))
    success = make_test_data(user_id, task_id, test_data_id)
    return make_response(jsonify({"user_id": user_id, "task_id": task_id, "end": success}), 200)



@app.route('/api/get_requests', methods=['POST'])
def get_requests_():
    data = request.get_json()
    user_id = str(data.get('user_id'))
    task_data = get_questions_by_task(user_id)
    return make_response(jsonify(task_data), 200)



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


# table にでバック用のデータを入れるため
# @app.route('/api/make_test', methods=['POST'])
# def make_test_():
#     test_df = pd.read_csv("test.csv",header=None)
#     data_df = pd.read_csv("annotate.csv",header=None)

#     task_dict = {
#         "user_id": 1,
#         "title": "機械翻訳の評価",
#         "description": "英日翻訳の正確さを3段階で評価してください",
#         "question_count": 2,
#         "questions": [
#             {
#                 "question": "正確さ",
#                 "scale_discription": [
#                     "原文の意味をほとんどまたは全く伝えていない。",
#                     "原文の意味の半分以上は伝えているが、重要な情報の抜けや軽微な誤訳がある。",
#                     "原文の意味を完全に伝えており、情報の欠落や誤訳がまったくない。"
#                 ]
#             },
#             {
#                 "question": "流暢性",
#                 "scale_discription": [
#                     "いい感じ",
#                     "全然ダメ"
#                 ]
#             }
#         ],
#         "private": True,
#         "start_day": "2025-08-01",
#         "end_day": "2025-08-07",
#         "max_annotations_per_user": 100,
#         "test": True,
#         "threshold": 0.5,
#         "test_data": test_df,   # pandas.DataFrame
#         "data": data_df         # pandas.DataFrame
#     }
#     create_task(task_dict)
#     return jsonify({"success":"good luck!"}), 200
