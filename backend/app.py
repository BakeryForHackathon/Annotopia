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
        {"task_id": 2, "title": "画像アノテーション作業", "status": "100%", "created_at": "2025-07-15", "due_date": "2025-07-25"},
        {"task_id": 3, "title": "テキストデータの分類", "status": "20%", "created_at": "2025-08-05", "due_date": "2025-08-20"},
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


# --- Helper Functions (Existing) ---
def is_test_ended(user_id, task_id):
    """ユーザーが特定のタスクのテストを完了したかどうかを判定します"""
    return TEST_COMPLETION_STATUS.get((str(user_id), str(task_id)), False)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Renderのヘルスチェックに応答するためのエンドポイント"""
    return jsonify({"status": "ok"}), 200
############################
# ===== 解決1: アノテーションデータ取得API =====
@app.route('/api/get_test_data', methods=['POST'])
def get_test_data():
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
        # ユーザーがまだアノテーションしておらず、他の誰も予約していないデータを検索
        if item_id not in user_annotated_ids and (task_id, item_id) not in ANNOTATION_RESERVATIONS:
            next_data = item
            break

    # アノテーションするデータがない場合
    if next_data is None:
        return jsonify({"success": True, "end": True})

    # データが見つかった場合、そのデータを現在のユーザーのために予約
    ANNOTATION_RESERVATIONS[(task_id, next_data['test_data_id'])] = user_id
    app.logger.info(f"Data {next_data['test_data_id']} for task {task_id} reserved by user {user_id}")

    annotated_count = len(user_annotated_ids)
    max_annotations = DUMMY_TASK_DETAILS.get(task_id, {}).get("max_annotations_per_user", len(task_data_list))
    status = "0%"
    if max_annotations > 0:
        status = f"{round((annotated_count / max_annotations) * 100)}%"

    # フロントエンドの要求に合わせたJSONレスポンスを構築
    response = {
        "success": True,
        "end": False,
        "user_id": user_id,
        "task_id": task_id,
        "test_data_id": next_data['test_data_id'],
        "data": next_data['data'],
        "data_count": annotated_count,
        "status": status,
        "questions": DUMMY_ANNOTATION_QUESTIONS.get(task_id, [])
    }
    return jsonify(response)

# ===== 解決2: アノテーションデータ送信API =====
@app.route('/api/get_make_data', methods=['POST'])
def get_make_data():
    """アノテーション結果を保存し、終了判定を行う"""
    data = request.get_json()
    user_id = str(data.get('user_id'))
    task_id = str(data.get('task_id'))
    test_data_id = data.get('test_data_id')
    answers = data.get('answers') # フロントから送られてくるanswersを受け取る

    # ユーザーとタスクIDをキーとしてアノテーション済みIDを保存
    key = (user_id, task_id)
    if key not in USER_ANNOTATIONS:
        USER_ANNOTATIONS[key] = []
    USER_ANNOTATIONS[key].append(test_data_id)
    app.logger.info(f"User {user_id} submitted annotation for data {test_data_id} with answers {answers}")

    # 処理が完了したので、このデータの予約を解除
    if (task_id, test_data_id) in ANNOTATION_RESERVATIONS:
        del ANNOTATION_RESERVATIONS[(task_id, test_data_id)]

    # 終了条件の判定
    annotated_count = len(USER_ANNOTATIONS[key])
    max_annotations = DUMMY_TASK_DETAILS.get(task_id, {}).get("max_annotations_per_user", 0)

    is_ended = annotated_count >= max_annotations

    # フロントエンドの要求に合わせたJSONレスポンスを返す
    return jsonify({
        "success": True,
        "user_id": user_id,
        "task_id": task_id,
        "end": is_ended
    })

# ===== 解決3: タスク詳細取得API =====
@app.route('/api/task_detail', methods=['POST'])
def get_task_detail():
    """タスクIDに基づき詳細情報を取得し、テスト完了状態を付与して返す"""
    data = request.get_json()
    user_id = str(data.get('user_id'))
    task_id = str(data.get('task_id'))

    task_detail = DUMMY_TASK_DETAILS.get(task_id)
    if not task_detail:
        return jsonify({"success": False, "message": "Task not found"}), 404

    # フロントの要求に合わせてレスポンスデータを構築
    response_data = task_detail.copy()
    response_data['user_id'] = user_id
    response_data['task_id'] = task_id
    response_data['question_count'] = len(response_data.get('questions', []))

    # キーの名前を'test_ended'から'ended'に変更
    response_data['ended'] = is_test_ended(user_id, task_id)

    return jsonify(response_data)


# ===== 解決4: テスト開始API =====
@app.route('/api/test_copy', methods=['POST'])
def test_copy():
    """テストデータの準備（コピー処理などを想定）を行う"""
    data = request.get_json()
    user_id = str(data.get('user_id'))
    task_id = str(data.get('task_id'))

    # ここに本来であれば、ユーザー用のテストデータをDBにコピーするなどの処理を記述
    app.logger.info(f"Test initiated for user_id: {user_id}, task_id: {task_id}")

    return jsonify({
        "success": True,
        "user_id": user_id,
        "task_id": task_id
    })

# ===== 解決5: qwkのAPI =====
@app.route('/api/get_qwk', methods=['POST'])
def get_qwk():
    """アノテーションの評価結果（QWKスコア）を指定の形式で返す"""
    data = request.get_json()
    user_id = str(data.get('user_id'))
    task_id = str(data.get('task_id'))

    # --- QWKスコア計算ロジック（ダミー） ---
    # ここに実際のユーザーの回答と正解データを基にしたQWK計算ロジックを実装します。
    # この例では、ダミーの固定値を返します。
    dummy_qwk_score = 0.9
    is_clear = dummy_qwk_score >= 0.6  # 例: QWK 0.6以上で合格

    # タスク詳細から質問項目名を取得
    task_details = DUMMY_TASK_DETAILS.get(task_id, {})
    # 質問項目が複数ある場合も考慮できますが、今回は最初の質問のみを対象とします。
    question_text = "未定義の質問"
    if task_details and task_details.get("questions"):
        question_text = task_details["questions"][0].get("question", "質問名なし")
    # --- ここまでがダミーロジック ---

    # ご指定のJSON形式でレスポンスを構築
    response_data = {
        "user_id": user_id,
        "task_id": task_id,
        "qwk_data": [
            {
                "question": question_text,
                "qwk": dummy_qwk_score,
                "clear": is_clear
            }
        ]
        # 複数の評価項目がある場合は、このリストにオブジェクトを追加します。
        # e.g.,
        # {
        #     "question": "流暢さ",
        #     "qwk": 0.75,
        #     "clear": True
        # }
    }

    return jsonify(response_data)

@app.route('/api/login', methods=['POST'])
def login_user(): return jsonify({"success": True, "token": "dummy-token", "user": {"id": 3, "name": "Taro"}}), 200
@app.route('/api/all_requests', methods=['POST'])
def get_all_requests(): return jsonify({"user_id": str(request.get_json().get('user_id')), "tasks": DUMMY_TASKS.get(str(request.get_json().get('user_id')), [])}), 200

# ===== 解決6: アノテーションデータ送信API =====
@app.route('/api/get_annotation_data', methods=['POST'])
def get_annotation_data():
    """未アノテーションのデータを1件取得し、予約する"""
    data = request.get_json()
    user_id = str(data.get('user_id'))
    task_id = str(data.get('task_id'))

    task_data_list = DUMMY_ANNOTATION_DATA.get(task_id, [])
    if not task_data_list:
        return jsonify({"message": "タスクデータが見つかりません。"}), 404

    user_annotated_ids = set(USER_ANNOTATIONS.get((user_id, task_id), []))

    next_data = None
    for item in task_data_list:
        item_id = item['test_data_id']
        if item_id not in user_annotated_ids and (task_id, item_id) not in ANNOTATION_RESERVATIONS:
            next_data = item
            break

    # 全てのアノテーションが完了している場合
    if next_data is None:
        return jsonify({"end": True})

    # 予約処理
    ANNOTATION_RESERVATIONS[(task_id, next_data['test_data_id'])] = user_id
    app.logger.info(f"Data {next_data['test_data_id']} for task {task_id} reserved by user {user_id}")

    # レスポンスデータを構築
    annotated_count = len(user_annotated_ids)
    max_annotations = DUMMY_TASK_DETAILS.get(task_id, {}).get("max_annotations_per_user", len(task_data_list))
    status = f"{round((annotated_count / max_annotations) * 100)}%" if max_annotations > 0 else "0%"

    response = {
        "user_id": user_id,
        "task_id": task_id,
        # キー名を test_data_id から annotation_data_id に変更してフロントと合わせる
        "annotation_data_id": next_data['test_data_id'],
        "data": next_data['data'],
        "data_count": annotated_count,
        "status": status,
        "questions": DUMMY_ANNOTATION_QUESTIONS.get(task_id, [])
    }
    return jsonify(response)

# ===== 解決7: アノテーションデータ送信API =====
@app.route('/api/get_make_annotation_data', methods=['POST'])
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

    if annotation_data_id not in USER_ANNOTATIONS[key]:
        USER_ANNOTATIONS[key].append(annotation_data_id)

    app.logger.info(f"User {user_id} submitted annotation for data {annotation_data_id} with answers {answers}")

    if (task_id, annotation_data_id) in ANNOTATION_RESERVATIONS:
        del ANNOTATION_RESERVATIONS[(task_id, annotation_data_id)]

    annotated_count = len(USER_ANNOTATIONS[key])
    max_annotations = DUMMY_TASK_DETAILS.get(task_id, {}).get("max_annotations_per_user", 0)

    is_ended = annotated_count >= max_annotations

    # success キーを削除
    return jsonify({
        "user_id": user_id,
        "task_id": task_id,
        "end": is_ended
    })

@app.route('/api/is_annotation_ended', methods=['POST'])
def is_annotation_ended_api():
    """
    ユーザーのアノテーション作業がノルマに達したかを確認するAPI。
    """
    data = request.get_json()
    user_id = str(data.get('user_id'))
    task_id = str(data.get('task_id'))

    # ユーザーがこれまでにアノテーションした数を取得
    key = (user_id, task_id)
    annotated_count = len(USER_ANNOTATIONS.get(key, []))
    
    # タスクのノルマ（最大アノテーション数）を取得
    task_details = DUMMY_TASK_DETAILS.get(task_id, {})
    # ノルマが設定されていない場合は、全データ数をノルマとする
    max_annotations = task_details.get("max_annotations_per_user", len(DUMMY_ANNOTATION_DATA.get(task_id, [])))

    # アノテーション済み個数がノルマ以上であれば True を返す
    is_ended = annotated_count >= max_annotations

    return jsonify({
        "user_id": user_id,
        "task_id": task_id,
        "end": is_ended
    })

@app.route('/api/upload_task', methods=['POST'])
def create_task(): return jsonify({"success": True, "task_id": 4})

@app.route('/api/requests', methods=['POST'])
def get_requests():
    """発注済みの依頼リストを返す"""
    data = request.get_json()
    user_id = str(data.get('user_id'))
    
    # DUMMY_TASKS を使わずに、ここで直接ダミーデータを作成
    tasks = [
        {"task_id": 1, "title": "【ダミー】機械翻訳の評価", "status": "50%", "created_at": "2025-08-01", "due_date": "2025-08-07"},
        {"task_id": 2, "title": "【ダミー】画像アノテーション作業", "status": "100%", "created_at": "2025-07-15", "due_date": "2025-07-25"},
        {"task_id": 3, "title": "【ダミー】テキストデータの分類", "status": "20%", "created_at": "2025-08-05", "due_date": "2025-08-20"},
        {"task_id": 4, "title": "【ダミー】音声データの文字起こし", "status": "依頼準備中", "created_at": "2025-07-20", "due_date": "2025-07-30"},
    ]
    
    return jsonify({
        "user_id": user_id,
        "tasks": tasks
    })

############################



if __name__ == '__main__':
    app.run(debug=True, port=5001)