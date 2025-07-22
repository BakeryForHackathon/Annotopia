from flask import Flask
from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from auth_utils import authenticate_user 
from make_request_table import get_requests  

app = Flask(__name__, static_folder="./build/static", template_folder="./build")
CORS(app) #Cross Origin Resource Sharing

@app.route("/", methods=['GET', 'HEAD']) # GETとHEADメソッドを許可
def home():
    if request.method == 'HEAD':
        return make_response("", 200)
    
    user_id = 1 # ここでは仮のユーザーIDを使用しています。実際のアプリケーションでは、認証後に取得したユーザーIDを使用してください。
    tasks = get_requests(user_id)
    if tasks:
        response_data = {
            "success": True,
            "message": "タスク情報の取得に成功しました。",
            "tasks": tasks
        }
        return make_response(jsonify(response_data), 200)
    # username_to_test = "user1"
    # password_to_test = "password1" # auth_utils.pyのMOCK_USERSまたはDBのパスワードに合わせる

    # authenticated_user = authenticate_user(username_to_test, password_to_test)
    # if authenticated_user:
    #     token = "eyJhbGciOiJIUzI1NiIs..." 
    #     response_data = {
    #         "success": True,
    #         "message": f"ユーザー '{username_to_test}' の認証に成功しました。",
    #         "token": token,
    #         "user": {
    #             "id": authenticated_user["id"]
    #         }
    #     }
    #     return make_response(jsonify(response_data), 200)
    # else:
    #     response_data = {
    #         "success": False,
    #         "message": f"ユーザー '{username_to_test}' の認証に失敗しました。無効なユーザー名またはパスワードです。",
    #         "token": None,
    #         "user": None
    #     }
    #     return make_response(jsonify(response_data), 401) # 401 Unauthorized


@app.route('/api/login', methods=['POST'])
def login_user():
    data = request.get_json()
    
    # Debug
    print("Received login request:", data)
    
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