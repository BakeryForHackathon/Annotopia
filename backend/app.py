from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import os
import json

app = Flask(__name__)

# --- App Configuration (Existing) ---
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app, supports_credentials=True)
app.logger.setLevel(logging.DEBUG)


# --- Dummy Database (Existing) ---
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
# 受注者のテスト完了状況
TEST_COMPLETION_STATUS = { ("3", "2"): True }
next_task_id = 4


# --- Helper Functions (Existing) ---
def is_test_ended(user_id, task_id):
    """ユーザーが特定のタスクのテストを完了したかどうかを判定します"""
    return TEST_COMPLETION_STATUS.get((str(user_id), str(task_id)), False)


# --- API Endpoints (Existing) ---

@app.route('/api/login', methods=['POST'])
def login_user():
    app.logger.info("--- /api/login endpoint hit ---")
    data = request.get_json()
    user_data = DUMMY_USERS.get(data.get('username'))
    if user_data and user_data["password_plain"] == data.get('password'):
        return jsonify({"success": True, "token": "dummy-token", "user": {"id": user_data["id"], "name": data.get('username')}}), 200
    return jsonify({"success": False, "message": "Invalid credentials"}), 401

@app.route('/api/all_requests', methods=['POST'])
def get_all_requests():
    app.logger.info("--- /api/all_requests endpoint hit ---")
    data = request.get_json()
    user_id = str(data.get('user_id'))
    user_tasks = DUMMY_TASKS.get(user_id, [])
    return jsonify({"user_id": user_id, "tasks": user_tasks}), 200

@app.route('/api/task_detail', methods=['POST'])
def get_task_detail():
    app.logger.info("--- /api/task_detail endpoint hit ---")
    data = request.get_json()
    user_id = str(data.get('user_id'))
    task_id = str(data.get('task_id'))
    task_detail = DUMMY_TASK_DETAILS.get(task_id)
    if not task_detail:
        return jsonify({"success": False, "message": "Task not found"}), 404
    response_data = task_detail.copy()
    response_data['test_ended'] = is_test_ended(user_id, task_id)
    return jsonify(response_data), 200

@app.route('/api/get_test', methods=['POST'])
def get_test():
    app.logger.info("--- /api/get_test endpoint hit ---")
    data = request.get_json()
    task_id = str(data.get('task_id'))
    test_data = DUMMY_TEST_DATA.get(task_id)
    if not test_data:
        return jsonify({"success": False, "message": "Test data not found"}), 404
    task_detail = DUMMY_TASK_DETAILS.get(task_id)
    return jsonify({"test_info": test_data, "task_detail": task_detail}), 200

@app.route('/api/submit_test', methods=['POST'])
def submit_test():
    app.logger.info("--- /api/submit_test endpoint hit ---")
    data = request.get_json()
    user_id = str(data.get('user_id'))
    task_id = str(data.get('task_id'))
    score = 60
    passed = score >= 50
    if passed:
        TEST_COMPLETION_STATUS[(user_id, task_id)] = True
    return jsonify({"success": True, "score": score, "passed": passed})

@app.route('/api/upload_task', methods=['POST'])
def create_task():
    global next_task_id
    app.logger.info("--- /api/upload_task endpoint hit ---")
    try:
        user_id = request.form.get('user_id')
        title = request.form.get('title')
        description = request.form.get('description')
        questions_json = request.form.get('questions')
        end_day = request.form.get('end_day')
        max_annotations = request.form.get('max_annotations_per_user')
        test_data_file = request.files.get('test_data')
        data_file = request.files.get('data')

        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
        if test_data_file and test_data_file.filename != '':
            test_data_file.save(os.path.join(app.config['UPLOAD_FOLDER'], test_data_file.filename))
        if data_file and data_file.filename != '':
            data_file.save(os.path.join(app.config['UPLOAD_FOLDER'], data_file.filename))

        new_task_id_str = str(next_task_id)
        if user_id not in DUMMY_TASKS:
            DUMMY_TASKS[user_id] = []
        DUMMY_TASKS[user_id].append({
            "task_id": next_task_id, "title": title, "status": "準備中",
            "created_at": "2025-07-26", "due_date": end_day or 'N/A'
        })
        DUMMY_TASK_DETAILS[new_task_id_str] = {
            "title": title, "description": description,
            "questions": json.loads(questions_json) if questions_json else [],
            "start_day": "2025-07-26", "end_day": end_day or 'N/A',
            "max_annotations_per_user": max_annotations
        }
        TEST_COMPLETION_STATUS[(user_id, new_task_id_str)] = False
        
        next_task_id += 1
        return jsonify({"success": True, "task_id": int(new_task_id_str)})
    except Exception as e:
        app.logger.error(f"Error in /api/upload_task: {e}")
        return jsonify({"success": False, "message": "An internal error occurred."}), 500

# --- ✨ ここから追記 ---

# 発注者が作成した正解データを保存する場所
MASTER_ANSWERS = {}

@app.route('/api/submit_master_answers', methods=['POST'])
def submit_master_answers():
    """発注者が作成したテストの正解データを受け取り保存する"""
    app.logger.info("--- /api/submit_master_answers endpoint hit ---")
    data = request.get_json()
    task_id = str(data.get('task_id'))
    answers = data.get('answers')

    # 正解データを保存
    MASTER_ANSWERS[task_id] = answers
    
    app.logger.info(f"Master answers for task_id {task_id} have been saved.")
    app.logger.info(f"Current Master Answers: {MASTER_ANSWERS}")
    
    return jsonify({"success": True, "message": "正解データを保存しました。"})


if __name__ == '__main__':
    app.run(debug=True, port=5001)
