import logging
from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from auth_utils import authenticate_user 
from make_request_table import get_requests  
from create_task import create_task  # Import the create_task function
import pandas as pd
from debag import fetch_all_from_table  # Import the function to fetch data from tables
from utils.get_ids import get_ids_by_task_id  # Import the function to count questions
from utils.set_test_data import set_test_data  # Import the function to set test data
from utils.get_requests import get_questions_by_task  # Import the function to get questions by task ID
from utils.get_randam_test_id import select_random_unanswered_test  # Import the function to select random unanswered test
from get_test_data import get_test_data  # Import the function to get test data   
from make_test import make_test_data  # Import the function to make test data
from is_ended import is_test_ended  # Import the function to check if the test is ended
from get_all_requests import get_all_requests  # Import the function to get all requests
from get_task_detail import get_task_detail  # Import the function to get task detail
from test_copy import test_copy  # Import the function to copy test data
from get_qwk import get_qwk  # Import the function to get QWK data


app = Flask(__name__)
CORS(app, supports_credentials=True)
app.logger.setLevel(logging.DEBUG)

# --- ダミーデータ ---
DUMMY_USERS = {
    "Taro": {"id": 3, "password_plain": "password123"}
}
DUMMY_TASKS = {
    "3": [
        {"task_id": 1, "title": "機械翻訳の評価", "status": "50%", "created_at": "2025-08-01", "due_date": "2025-08-07"},
        {"task_id": 2, "title": "画像アノテーション作業", "status": "完了", "created_at": "2025-07-15", "due_date": "2025-07-25"},
        {"task_id": 3, "title": "テキストデータの分類", "status": "依頼準備中", "created_at": "2025-08-05", "due_date": "2025-08-20"},
    ]
}
DUMMY_TASK_DETAILS = {
    "1": {
        "title": "機械翻訳の評価", "description": "英日翻訳の正確さを3段階で評価してください", "question_count": 1,
        "questions": [{"question": "正確さ", "scale_discription": ["1:原文の意味をほとんどまたは全く伝えていない。意味が通らないか、全く異なる内容になっている。", "2:原文の意味の半分以上は伝えているが、重要な情報の抜けや軽微な誤訳がある。", "3:原文の意味を完全に伝えており、情報の欠落や誤訳がまったくない。"]}],
        "start_day": "2025/08/01", "end_day": "2025/08/07", "max_annotations_per_user": 100
    }
}
DUMMY_TEST_DATA = {
    "1": {
        "total_questions": 2,
        "questions": [
            {"id": 1, "source_text": "The quick brown fox jumps over the lazy dog.", "translated_text": "速い茶色のキツネは怠惰な犬を飛び越えます。"},
            {"id": 2, "source_text": "Never underestimate the power of a good book.", "translated_text": "良い本の力を過小評価しないでください。"}
        ]
    }
}
TEST_COMPLETION_STATUS = {
    ("3", "2"): False,
}

def is_test_ended(user_id, task_id):
    """ユーザーが特定のタスクのテストを完了したかどうかを判定します"""
    return TEST_COMPLETION_STATUS.get((str(user_id), str(task_id)), False)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Renderのヘルスチェックに応答するためのエンドポイント"""
    return jsonify({"status": "ok"}), 200

@app.route("/login", methods=['POST'])
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


@app.route('/api/all_requests', methods=['POST'])
def get_all_requests():
    data = request.get_json()
    user_id = str(data.get('user_id'))
    user_tasks = DUMMY_TASKS.get(user_id, [])
    return jsonify({"user_id": user_id, "tasks": user_tasks}), 200

@app.route('/api/task_detail', methods=['POST'])
def get_task_detail():
    data = request.get_json()
    user_id = str(data.get('user_id'))
    task_id = str(data.get('task_id'))
    task_detail = DUMMY_TASK_DETAILS.get(task_id)
    if not task_detail: return jsonify({"success": False, "message": "Task not found"}), 404
    task_detail['test_ended'] = is_test_ended(user_id, task_id)
    return jsonify(task_detail), 200

@app.route('/api/get_test', methods=['POST'])
def get_test():
    data = request.get_json()
    task_id = str(data.get('task_id'))
    test_data = DUMMY_TEST_DATA.get(task_id)
    if not test_data: return jsonify({"success": False, "message": "Test data not found"}), 404
    task_detail = DUMMY_TASK_DETAILS.get(task_id)
    return jsonify({"test_info": test_data, "task_detail": task_detail}), 200

@app.route('/api/submit_test', methods=['POST'])
def submit_test():
    data = request.get_json()
    user_id = str(data.get('user_id'))
    task_id = str(data.get('task_id'))
    answers = data.get('answers')

    score = 60 
    passed = score >= 50

    if passed:
        TEST_COMPLETION_STATUS[(user_id, task_id)] = True

    return jsonify({"success": True, "score": score, "passed": passed})
# --- ここまで追記 ---

if __name__ == '__main__':
    app.run(debug=True, port=5001)
