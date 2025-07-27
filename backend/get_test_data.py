"""
画面遷移時にテストデータを取得するためのコードを記述します。
dct = get_test_data(user_name, task_id) 
dct = {
  “user_id”
  “task_id”
   “test_data_id”
   “data”:原文: She went to the store to buy some milk.\n訳文: 彼女はミルクを買うために店に行った。
    “data_count” 0                   ←annotate済みのデータ数　　+1して問1にする
    status:”20%”
    questions : [
        {
             question:正確さ
             scale:
             scale_discription:[
                 原文の意味をほとんどまたは全く伝えていない。意味が通らないか、全く異なる内容になっている。,
                 原文の意味の半分以上は伝えているが、重要な情報の抜けや軽微な誤訳がある。,
                 原文の意味を完全に伝えており、情報の欠落や誤訳がまったくない。                  
             ]
     }
}
"""

from utils.get_ids import get_ids_by_task_id
from utils.connect_db import get_db_connection

import random
from utils.connect_db import get_db_connection
from utils.get_randam_test_id import get_unanswered_test_ids, get_answered_test_ids
from utils.get_requests import get_questions_by_task

def get_test_data(user_id, task_id):
    """
    ユーザーが未回答の test_data を1つ取得し、詳細情報を含む辞書を返す。
    """
    # 未回答のテストデータからランダムに1つ選択
    unanswered_ids = get_unanswered_test_ids(user_id, task_id)
    if not unanswered_ids:
        print("未回答のテストデータはありません。")
        return None

    test_data_id = random.choice(unanswered_ids)

    # 回答済みの件数を取得
    answered_ids = get_answered_test_ids(user_id,task_id)
    data_count = len(answered_ids)

    # DBから test_data の原文と訳文を取得、total_data_count も取得
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        if not conn:
            return None
        cur = conn.cursor()

        # test_data 取得
        cur.execute("""
            SELECT data FROM test_data
            WHERE id = %s
        """, (test_data_id,))
        row = cur.fetchone()
        if not row:
            print("該当する test_data が見つかりません。")
            return None

        data_str = row[0] 

        # total_data_count 取得
        
        total_data_count = len(get_ids_by_task_id(task_id, "test_data"))
        progress_percent = int((len(answered_ids) / total_data_count) * 100)

        # 質問一覧を取得
        questions = get_questions_by_task(task_id)


        # 結果の辞書
        dct = {
            "user_id": user_id,
            "task_id": task_id,
            "test_data_id": test_data_id,
            "data": data_str,
            "data_count": data_count,
            "status": f"{progress_percent}%",
            "questions": questions
        }
        return dct

    except Exception as e:
        print(f"get_test_data 実行中のエラー: {e}")
        return None
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
