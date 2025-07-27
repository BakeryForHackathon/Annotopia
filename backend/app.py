import logging
import io
import hashlib
from flask import Flask, request, make_response, jsonify, send_file
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
from get_task_annotated_data import get_task_annotated_data  # Import the function to get annotated data for a task


app = Flask(__name__)
CORS(app, origins="https://myapp-frontend-3p4k.onrender.com", supports_credentials=True)
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
        token = str(hashlib.sha256(username.encode()).hexdigest())
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
    return make_response(jsonify(task_detail), 200)

@app.route('/api/get_test_data', methods=['POST'])
def get_test_data_():
    data = request.get_json()
    user_id = str(data.get('user_id'))
    task_id = str(data.get('task_id'))
    answers = get_test_data(user_id, task_id)
    return make_response(jsonify(answers), 200)

# @app.route('/api/get_master_test_question', methods=['POST'])
# def get_master_test_question():
#     data = request.get_json()
#     user_id = str(data.get('user_id'))
#     task_id = str(data.get('task_id'))
#     test_data = get_test_data(user_id, task_id)
#     if not test_data: return jsonify({"success": False, "message": "Test data not found"}), 404
#     # task_detail = get_test_data(user_id, task_id)
#     return make_response(jsonify(test_data), 200)
#     # return jsonify({"test_info": test_data, "task_detail": task_detail}), 200

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
@app.route('/api/get_make_annotation_data', methods=['POST'])
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

# 要修正
import json
@app.route('/api/upload_task', methods=['POST'])
def create_task_():
    try:
        # フォームデータの取得
        user_id = request.form.get('user_id')
        title = request.form.get('title')
        description = request.form.get('description')
        question_count = int(request.form.get('question_count', 0))
        questions = json.loads(request.form.get('questions', '[]'))
        private = request.form.get('private') == 'true'
        start_day = request.form.get('start_day')
        end_day = request.form.get('end_day')
        max_annotations_per_user = int(request.form.get('max_annotations_per_user', 1))
        test = request.form.get('test') == 'true'
        threshold = float(request.form.get('threshold', 0.5))

        # ファイルの取得とDataFrame化

        try:
            test_data_file = request.files.get('test_data')
            if test_data_file is None:
                raise ValueError("test_data ファイルがアップロードされていません。")
            test_df = pd.read_csv(test_data_file,header=None)
        except Exception as e:
            return jsonify({"success": False, "error": f"test_data ファイルの読み込みに失敗しました: {str(e)}"}), 400

        try:
            data_file = request.files.get('data')
            if data_file is None:
                raise ValueError("data ファイルがアップロードされていません。")
            data_df = pd.read_csv(data_file,header=None)
        except Exception as e:
            return jsonify({"success": False, "error": f"data ファイルの読み込みに失敗しました: {str(e)}"}), 400


        # 結果の辞書を構築
        dct = {
            "user_id": int(user_id),
            "title": title,
            "description": description,
            "question_count": question_count,
            "questions": questions,
            "private": private,
            "start_day": start_day,
            "end_day": end_day,
            "max_annotations_per_user": max_annotations_per_user,
            "test": test,
            "threshold": threshold,
            "test_data": test_df,
            "data": data_df
        }

        task_id = create_task(dct)  # create_task関数を呼び出してタスクを作成
        if not task_id:
            success = False
        else:
            success = True
        # 成功レスポンス
        return jsonify({
            "success": success,
            "user_id": dct["user_id"],
            "task_id": task_id
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/api/requests', methods=['POST'])
def get_requests_():
    data = request.get_json()
    user_id = str(data.get('user_id'))
    requests = get_requests(user_id)
    return make_response(jsonify(requests), 200)


@app.route('/api/finalize_task', methods=['POST'])
def download_():
    data = request.get_json()
    task_id = str(data.get('task_id'))
    requests_df = get_task_annotated_data(task_id)  # DataFrameで返る前提

    # CSVに変換
    csv_buffer = io.StringIO()
    requests_df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)

    filename = f"task_{task_id}_result.csv"
    return send_file(
        io.BytesIO(csv_buffer.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name=filename
    )

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

@app.route('/api/debag_create_task', methods=['POST'])
def debag_create_task_():
    test_df = pd.read_csv("test.csv",header=None)
    data_df = pd.read_csv("annotate.csv",header=None)
    task_dict = {
        "user_id": 1,
        "title": "機械翻訳の評価",
        "description": "英日翻訳の正確さを3段階で評価してください",
        "question_count": 2,
        "questions": [
            {
                "question": "正確さ",
                "scale_discription": [
                    "原文の意味をほとんどまたは全く伝えていない。",
                    "原文の意味の半分以上は伝えているが、重要な情報の抜けや軽微な誤訳がある。",
                    "原文の意味を完全に伝えており、情報の欠落や誤訳がまったくない。"
                ]
            },
            {
                "question": "流暢性",
                "scale_discription": [
                    "いい感じ",
                    "全然ダメ"
                ]
            }
        ],
        "private": True,
        "start_day": "2025-08-01",
        "end_day": "2025-08-07",
        "max_annotations_per_user": 100,
        "test": True,
        "threshold": 0.5,
        "test_data": test_df,   # pandas.DataFrame
        "data": data_df         # pandas.DataFrame
    }

if __name__ == '__main__':
    app.run(debug=True, port=5001)
