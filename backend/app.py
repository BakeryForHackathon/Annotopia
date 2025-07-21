from flask import Flask, request, jsonify
from flask_cors import CORS
# 実際のアプリではパスワードハッシュのためにインポートします
# from werkzeug.security import check_password_hash 

app = Flask(__name__)
CORS(app)

# ダミーのユーザーデータベースの代わり
# 実際にはデータベースからユーザー情報を取得します
DUMMY_USERS = {
    "Taro": {
        "id": 3,
        "password_hash": "...", # 本来はハッシュ化されたパスワード
        "password_plain": "password123" # サンプル用の平文パスワード
    }
}

@app.route('/api/login', methods=['POST'])
def login_user():
    # フロントエンドから送信されたJSONデータを取得
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Invalid request"}), 400

    username = data.get('username')
    password = data.get('password')

    # ユーザー名とパスワードの存在をチェック
    user_data = DUMMY_USERS.get(username)

    # ユーザーが存在し、パスワードが一致する場合
    # ⚠️ 重要: 実際にはハッシュ化されたパスワードを比較します
    if user_data and user_data["password_plain"] == password:
        # ログイン成功時のレスポンス
        # トークンはJWTなどを使って生成するのが一般的です
        response_data = {
            "success": True,
            "token": "esafda-generated-token", # ダミーのトークン
            "user": {
                "id": user_data["id"],
                "name": username,
            }
        }
        return jsonify(response_data), 200
    else:
        # ログイン失敗時のレスポンス
        response_data = {
            "success": False,
            "token": None,
            "user": None
        }
        return jsonify(response_data), 401 # 401 Unauthorized

if __name__ == '__main__':
    app.run(debug=True, port=5001) # フロントエンドと違うポートで実行