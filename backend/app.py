# app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
import logging

app = Flask(__name__)

# --- App Configuration (Existing) ---
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app, supports_credentials=True)
app.logger.setLevel(logging.DEBUG)


# --- Dummy Database (Existing) ---
DUMMY_USERS = {"Taro": {"id": 3, "password_plain": "password123"}}
DUMMY_TASKS = {
    "3": [
        {"task_id": 1, "title": "機械翻訳の評価", "status": "50%", "created_at": "2025-08-01", "due_date": "2025-08-07"},
        {"task_id": 2, "title": "画像アノテーション作業", "status": "完了", "created_at": "2025-07-15", "due_date": "2025-07-25"},
        {"task_id": 3, "title": "テキストデータの分類", "status": "依頼準備中", "created_at": "2025-08-05", "due_date": "2025-08-20"},
    ]
}
DUMMY_TASK_DETAILS = {
    "1": {
        "title": "機械翻訳の評価", "description": "英日翻訳の正確さを3段階で評価してください",
        "questions": [{"question": "正確さ", "scale_discription": [
            {"score": 1, "description": "1:原文の意味をほとんどまたは全く伝えていない。"},
            {"score": 2, "description": "2:原文の意味の半分以上は伝えているが、重要な情報の抜けや軽微な誤訳がある。"},
            {"score": 3, "description": "3:原文の意味を完全に伝えており、情報の欠落や誤訳がまったくない。"},
        ]}], "start_day": "2025/08/01", "end_day": "2025/08/07", "max_annotations_per_user": 100
    }
}
DUMMY_TEST_DATA = {
    "1": {
        "total_questions": 2,
        "questions": [
            {
                "id": 1, 
                "text": "原文: The quick brown fox jumps over the lazy dog.\n機械翻訳: 速い茶色のキツネは怠惰な犬を飛び越えます。"
            },
            {
                "id": 2,
                "text": "原文: Never underestimate the power of a good book.\n機械翻訳: 良い本の力を過小評価しないでください。"
            }
        ]
    }
}
DUMMY_ANNOTATION_QUESTIONS = {
    "1": [{"question": "正確さ", "details": [
        {"question_details_id": 101, "scale": 3, "scale_description": "3: 原文の意味を完全に伝えており、情報の欠落や誤訳がまったくない。"},
        {"question_details_id": 102, "scale": 2, "scale_description": "2: 原文の意味の半分以上は伝えているが、重要な情報の抜けや軽微な誤訳がある。"},
        {"question_details_id": 103, "scale": 1, "scale_description": "1: 原文の意味をほとんどまたは全く伝えていない。"},
    ]}]
}
DUMMY_ANNOTATION_DATA = {
    "1": [
        {"test_data_id": 1, "data": "原文: She went to the store to buy some milk.\n訳文: 彼女はミルクを買うために店に行った。", "annotations": {}},
        {"test_data_id": 2, "data": "原文: The concert was amazing and the crowd was energetic.\n訳文: コンサートは素晴らしく、観客はエネルギッシュだった。", "annotations": {}},
        {"test_data_id": 3, "data": "原文: He is studying computer science at a prestigious university.\n訳文: 彼は名門大学でコンピューターサイエンスを勉強している。", "annotations": {}},
        {"test_data_id": 4, "data": "原文: The new policy will be implemented next month.\n訳文: 新しい方針は来月実施されます。", "annotations": {}},
        {"test_data_id": 5, "data": "原文: Reading books is a great way to expand your vocabulary.\n訳文: 本を読むことは語彙を増やす素晴らしい方法です。", "annotations": {}},
    ]
}

# --- State Management (In-memory) ---
TEST_COMPLETION_STATUS = {("3", "2"): True}
USER_TEST_ANSWERS = {}      # テストの回答を保存
MASTER_ANSWERS = {}         # テストの正解を保存
USER_ANNOTATIONS = {}       # アノテーション作業の進捗を保存
ANNOTATION_RESERVATIONS = {}# アノテーション作業の予約を管理


# --- 基本API (変更なし) ---
def is_test_ended(user_id, task_id): return TEST_COMPLETION_STATUS.get((str(user_id), str(task_id)), False)
@app.route('/api/login', methods=['POST'])
def login_user(): return jsonify({"success": True, "token": "dummy-token", "user": {"id": 3, "name": "Taro"}}), 200
@app.route('/api/all_requests', methods=['POST'])
def get_all_requests(): return jsonify({"user_id": str(request.get_json().get('user_id')), "tasks": DUMMY_TASKS.get(str(request.get_json().get('user_id')), [])}), 200
@app.route('/api/task_detail', methods=['POST'])
def get_task_detail():
    data = request.get_json()
    user_id, task_id = str(data.get('user_id')), str(data.get('task_id'))
    task_detail = DUMMY_TASK_DETAILS.get(task_id)
    if not task_detail: return jsonify({"success": False, "message": "Task not found"}), 404
    response_data = task_detail.copy()
    response_data['test_ended'] = is_test_ended(user_id, task_id)
    return jsonify(response_data), 200
@app.route('/api/upload_task', methods=['POST'])
def create_task(): return jsonify({"success": True, "task_id": 4})


# --- 受注者・発注者用テスト API (変更なし) ---
@app.route('/api/get_test_question', methods=['POST'])
def get_test_question():
    data = request.get_json()
    user_id, task_id = str(data.get('user_id')), str(data.get('task_id'))
    answers = USER_TEST_ANSWERS.get((user_id, task_id), [])
    question_index = len(answers)
    test_info = DUMMY_TEST_DATA.get(task_id)
    if not test_info or question_index >= test_info["total_questions"]: return jsonify({"success": True, "end": True})
    status = f"{round((question_index / test_info['total_questions']) * 100)}%"
    current_question = test_info["questions"][question_index]
    task_details = DUMMY_TASK_DETAILS.get(task_id)
    return jsonify({"success": True, "end": False, "question": current_question, "question_index": question_index, "total_questions": test_info["total_questions"], "status": status, "task_details": task_details})

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
    task_id = str(data.get('task_id'))
    answers = MASTER_ANSWERS.get(task_id, [])
    question_index = len(answers)
    test_info = DUMMY_TEST_DATA.get(task_id)
    if not test_info or question_index >= test_info["total_questions"]: return jsonify({"success": True, "end": True})
    status = f"{round((question_index / test_info['total_questions']) * 100)}%"
    current_question = test_info["questions"][question_index]
    task_details = DUMMY_TASK_DETAILS.get(task_id)
    return jsonify({"success": True, "end": False, "question": current_question, "question_index": question_index, "total_questions": test_info["total_questions"], "status": status, "task_details": task_details})

@app.route('/api/submit_master_answer', methods=['POST'])
def submit_master_answer():
    data = request.get_json()
    task_id = str(data.get('task_id'))
    answer = data.get('answer')
    if task_id not in MASTER_ANSWERS: MASTER_ANSWERS[task_id] = []
    MASTER_ANSWERS[task_id].append(answer)
    total_questions = DUMMY_TEST_DATA.get(task_id, {}).get("total_questions", 0)
    if len(MASTER_ANSWERS[task_id]) >= total_questions:
        app.logger.info(f"Master answers for task {task_id} completed: {MASTER_ANSWERS[task_id]}")
        return jsonify({"success": True, "end": True})
    return jsonify({"success": True, "end": False})


# --- アノテーション作業用 API (変更なし) ---
@app.route('/api/get_annotation_data', methods=['POST'])
def get_annotation_data():
    """未アノテーションのデータを1件取得し、予約する"""
    data = request.get_json()
    user_id = str(data.get('user_id'))
    task_id = str(data.get('task_id'))

    task_data_list = DUMMY_ANNOTATION_DATA.get(task_id, [])
    if not task_data_list:
        return jsonify({"success": False, "message": "タスクデータが見つかりません。"}), 404

    user_annotated_ids = set(USER_ANNOTATIONS.get((user_id, task_id), []))

    next_data = None
    for item in task_data_list:
        item_id = item['test_data_id']
        if item_id not in user_annotated_ids and (task_id, item_id) not in ANNOTATION_RESERVATIONS:
            next_data = item
            break
    
    if next_data is None:
        return jsonify({"success": True, "end": True})

    ANNOTATION_RESERVATIONS[(task_id, next_data['test_data_id'])] = user_id
    app.logger.info(f"Data {next_data['test_data_id']} for task {task_id} reserved by user {user_id}")

    annotated_count = len(user_annotated_ids)
    max_annotations = DUMMY_TASK_DETAILS.get(task_id, {}).get("max_annotations_per_user", len(task_data_list))
    status = f"{round((annotated_count / max_annotations) * 100)}%"

    response = {
        "success": True, "end": False, "user_id": user_id, "task_id": task_id,
        "annotation_data_id": next_data['test_data_id'],
        "data": next_data['data'],
        "data_count": annotated_count, "status": status,
        "questions": DUMMY_ANNOTATION_QUESTIONS.get(task_id, [])
    }
    return jsonify(response)


@app.route('/api/make_annotation_data', methods=['POST'])
def make_annotation_data():
    """アノテーション結果を保存し、終了判定を行う"""
    data = request.get_json()
    user_id = str(data.get('user_id'))
    task_id = str(data.get('task_id'))
    annotation_data_id = data.get('annotation_data_id')
    answers = data.get('answers')

    key = (user_id, task_id)
    if key not in USER_ANNOTATIONS:
        USER_ANNOTATIONS[key] = []
    USER_ANNOTATIONS[key].append(annotation_data_id)
    app.logger.info(f"User {user_id} submitted annotation for data {annotation_data_id} with answers {answers}")

    if (task_id, annotation_data_id) in ANNOTATION_RESERVATIONS:
        del ANNOTATION_RESERVATIONS[(task_id, annotation_data_id)]

    annotated_count = len(USER_ANNOTATIONS[key])
    max_annotations = DUMMY_TASK_DETAILS.get(task_id, {}).get("max_annotations_per_user", 0)
    
    is_ended = annotated_count >= max_annotations

    return jsonify({"success": True, "user_id": user_id, "task_id": task_id, "end": is_ended})


if __name__ == '__main__':
    app.run(debug=True, port=5001)