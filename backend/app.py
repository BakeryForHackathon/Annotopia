from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)

# --- ダミーデータ ---
DUMMY_USERS = {
    "Taro": {"id": 3, "password_plain": "password123"}
}
DUMMY_TASKS = {
    "3": [ # user_id = 3
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
        "total_questions": 2, # 問題数を2に減らしてテストしやすくします
        "questions": [
            {"id": 1, "source_text": "The quick brown fox jumps over the lazy dog.", "translated_text": "速い茶色のキツネは怠惰な犬を飛び越えます。"},
            {"id": 2, "source_text": "Never underestimate the power of a good book.", "translated_text": "良い本の力を過小評価しないでください。"}
        ]
    }
}

# --- ✨ テスト完了状態を管理するグローバル変数 ---
# サーバーを再起動するとリセットされます
# 形式: {(user_id, task_id): True/False}
TEST_COMPLETION_STATUS = {
    ("3", "2"): False, # user 3はtask 2のテストを完了済み
}

# --- 補助関数 (is_test_endedを更新) ---
def is_test_ended(user_id, task_id):
    """ユーザーが特定のタスクのテストを完了したかどうかを判定します"""
    return TEST_COMPLETION_STATUS.get((str(user_id), str(task_id)), False)

# --- 既存のAPIエンドポイント (変更なし) ---
@app.route('/api/login', methods=['POST'])
def login_user():
    # ... 既存のコード ...
    data = request.get_json()
    user_data = DUMMY_USERS.get(data.get('username'))
    if user_data and user_data["password_plain"] == data.get('password'):
        return jsonify({"success": True, "token": "dummy-token", "user": {"id": user_data["id"], "name": data.get('username')}}), 200
    return jsonify({"success": False}), 401

@app.route('/api/all_requests', methods=['POST'])
def get_all_requests():
    # ... 既存のコード ...
    data = request.get_json()
    user_id = str(data.get('user_id'))
    user_tasks = DUMMY_TASKS.get(user_id, [])
    return jsonify({"user_id": user_id, "tasks": user_tasks}), 200

@app.route('/api/task_detail', methods=['POST'])
def get_task_detail():
    # ... 既存のコード ...
    data = request.get_json()
    user_id = str(data.get('user_id'))
    task_id = str(data.get('task_id'))
    task_detail = DUMMY_TASK_DETAILS.get(task_id)
    if not task_detail: return jsonify({"success": False, "message": "Task not found"}), 404
    task_detail['test_ended'] = is_test_ended(user_id, task_id)
    return jsonify(task_detail), 200

@app.route('/api/get_test', methods=['POST'])
def get_test():
    # ... 既存のコード ...
    data = request.get_json()
    task_id = str(data.get('task_id'))
    test_data = DUMMY_TEST_DATA.get(task_id)
    if not test_data: return jsonify({"success": False, "message": "Test data not found"}), 404
    task_detail = DUMMY_TASK_DETAILS.get(task_id)
    return jsonify({"test_info": test_data, "task_detail": task_detail}), 200

# --- ✨ ここから追記 ---
@app.route('/api/submit_test', methods=['POST'])
def submit_test():
    """
    テストの回答を受け取り、採点して結果を返す
    """
    data = request.get_json()
    user_id = str(data.get('user_id'))
    task_id = str(data.get('task_id'))
    answers = data.get('answers')

    # ダミーの採点ロジック
    # ここでは単純に固定のスコアを返します
    score = 60 
    passed = score >= 50

    # テストが合格した場合のみ、完了ステータスを更新
    if passed:
        TEST_COMPLETION_STATUS[(user_id, task_id)] = True

    return jsonify({"success": True, "score": score, "passed": passed})
# --- ここまで追記 ---

if __name__ == '__main__':
    app.run(debug=True, port=5001)
