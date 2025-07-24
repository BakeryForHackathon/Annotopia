from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
# from auth_utils import authenticate_user 
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

app = Flask(__name__, static_folder="./build/static", template_folder="./build")
CORS(app) #Cross Origin Resource Sharing

@app.route("/", methods=['GET', 'HEAD']) # GETとHEADメソッドを許可
def home():
    if request.method == 'HEAD':
        return make_response("", 200)


    # test_df = pd.read_csv("test.csv",header=None)
    # data_df = pd.read_csv("annotate.csv",header=None)

    # task_dict = {
    #     "user_id": 1,
    #     "title": "機械翻訳の評価",
    #     "description": "英日翻訳の正確さを3段階で評価してください",
    #     "question_count": 2,
    #     "questions": [
    #         {
    #             "question": "正確さ",
    #             "scale_discription": [
    #                 "原文の意味をほとんどまたは全く伝えていない。",
    #                 "原文の意味の半分以上は伝えているが、重要な情報の抜けや軽微な誤訳がある。",
    #                 "原文の意味を完全に伝えており、情報の欠落や誤訳がまったくない。"
    #             ]
    #         },
    #         {
    #             "question": "流暢性",
    #             "scale_discription": [
    #                 "いい感じ",
    #                 "全然ダメ"
    #             ]
    #         }
    #     ],
    #     "private": True,
    #     "start_day": "2025-08-01",
    #     "end_day": "2025-08-07",
    #     "max_annotations_per_user": 100,
    #     "test": True,
    #     "threshold": 0.5,
    #     "test_data": test_df,   # pandas.DataFrame
    #     "data": data_df         # pandas.DataFrame
    # }
    # success = get_questions_by_task (1)
    # print(success)
    # success = select_random_unanswered_test(1, 1)
    # print(success)
    # data = fetch_all_from_table("test_data")
    # if data is not None:
    #     for row in data:
    #         print(row)
    # else:
    #     print("取得失敗")

    # success = get_test_data(1,1)
    # success_list = []
    # success = make_test_data(1,2,[2,5])
    # success_list.append({"success": success, "message": "add test_2 is 2 and 5"})

    # success = is_test_ended(1, 1)
    # success_list.append({"success": success, "message": "is_ended test_2"})

    # success = make_test_data(1,3,[3,4])
    # success_list.append({"success": success, "message": "add test_3 is 3 and 4"})

    # success = is_test_ended(1, 1)
    # success_list.append({"success": success, "message": "is_ended test_3"})

    # success = make_test_data(1,4,[2,5])
    # success_list.append({"success": success, "message": "add test_4 is 2 and 5"})

    # success = is_test_ended(1, 1)
    # success_list.append({"success": success, "message": "is_ended test_4"})

    # success = make_test_data(1,5,[2,5])
    # success_list.append({"success": success, "message": "add test_5 is 2 and 5"})

    # success = is_test_ended(1, 1)
    # success_list.append({"success": success, "message": "is_ended test_5"})

    success = []
    success.append(test_copy(1,3))
    success.append(make_test_data(2,1,[1,4]))
    success.append(make_test_data(2,2,[2,5]))
    success.append(make_test_data(2,3,[3,5]))
    success.append(make_test_data(2,4,[1,5]))
    success.append(make_test_data(2,5,[2,5]))
    success.append(make_test_data(3,1,[1,4]))
    success.append(make_test_data(3,2,[2,5]))
    success.append(make_test_data(3,3,[3,4]))
    success.append(make_test_data(3,4,[2,5]))
    success.append(make_test_data(3,5,[2,5]))
    success.append(get_qwk(1, 1))
    success.append(get_qwk(2, 1))
    success.append(get_qwk(3, 1))
    


    if success:
        response_data = {
            "success": success,
            "message": "タスクの保存に成功しました。"
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
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


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
