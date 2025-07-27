"""
user_idとtask_idを引数にして
テストデータのうちuserが未回答なtest_idを一つランダムに取得する関数
"""
import random
from utils.connect_db import get_db_connection
from utils.get_ids import get_ids_by_task_id  # ← 実際のファイル構成に応じて調整してください

from utils.connect_db import get_db_connection

def get_answered_test_ids(user_id, task_id):
    """
    指定ユーザーとタスクに対応する、回答済みの test_id をセットで返す。
    question_detail_id が NULL でないもののみ対象。
    """
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        if not conn:
            return set()

        cur = conn.cursor()
        cur.execute("""
            SELECT DISTINCT td.test_id
            FROM test_details td
            JOIN test_data tdata ON td.test_id = tdata.id
            WHERE td.user_id = %s
              AND tdata.task_id = %s
              AND td.question_detail_id IS NOT NULL
        """, (user_id, task_id))
        
        return {row[0] for row in cur.fetchall()}

    except Exception as e:
        print(f"回答済みテストIDの取得中にエラー: {e}")
        return set()
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

from utils.get_ids import get_ids_by_task_id  # データベースからtest_dataの全IDを取得

def get_unanswered_test_ids(user_id, task_id):
    """
    指定ユーザー・タスクにおいて、まだ回答していない test_id をリストで返す。
    """
    all_test_ids = get_ids_by_task_id(task_id, "test_data")
    if not all_test_ids:
        print("該当する test_data がありません。")
        return []

    answered_ids = get_answered_test_ids(user_id,task_id)
    return list(set(all_test_ids) - answered_ids)

import random

def select_random_unanswered_test(user_id, task_id):
    """
    ユーザーがまだ回答していない test_data の中からランダムに 1 件の test_id を選んで返す。
    """
    unanswered_ids = get_unanswered_test_ids(user_id, task_id)
    if not unanswered_ids:
        print("未回答のテストデータはありません。")
        return None

    return random.choice(unanswered_ids)
