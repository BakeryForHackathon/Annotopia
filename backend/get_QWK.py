from utils.get_ids import get_ids_by_task_id
from utils.get_id import get_client_id_by_task, get_threshold_by_task_id
from utils.get_requests import get_questions_by_task
from utils.get_randam_test_id import get_unanswered_test_ids

def get_qwk(user_id, task_id):
    """
    指定された user_id と task_id に対するタスクの詳細情報を取得して返す。
    questions, ended は未実装。
    """
    client_id = get_client_id_by_task(task_id)
    if len(get_unanswered_test_ids(client_id, task_id)):
        print("クライアントの未回答テストデータがあります。")
        return None
    if len(get_unanswered_test_ids(user_id, task_id)):
        print("ユーザーの未回答テストデータがあります。")
        return None
    
    test_ids = get_ids_by_task_id(task_id, "test_data")
    questions = get_questions_by_task(task_id)
    question_map = {}
    question_group_dct = {}

    for idx, question in enumerate(questions):
        # question["details"] は辞書のリストなので、question_details_id のリストに変換
        question_group_dct[idx] = [detail['question_details_id'] for detail in question["details"]]
        question_map[idx] = question["question"]
        
    client_test_data = get_grouped_test_details(client_id, test_ids,question_group_dct)
    user_test_data = get_grouped_test_details(user_id, test_ids, question_group_dct)

    client_test_data = group_by_group_id(client_test_data)
    user_test_data = group_by_group_id(user_test_data)

    threshold = get_threshold_by_task_id(task_id)
    qwk_data = []

    total_flag = True

    for group_id in question_group_dct.keys():
        qwk = calculate_qwk(client_test_data[group_id], user_test_data[group_id])
        if qwk >= threshold:
            flag = True
        else:
            flag = False
            total_flag = False
        qwk_data.append({
            "question": question_map[group_id],
            "qwk": qwk,
            "clear": flag
        })
        
    if total_flag == False:
        delete_test_details_by_user_and_tests(user_id, test_ids)

    dct = {
        "user_id": user_id,
        "task_id": task_id,
        "qwk_data": qwk_data
    }
    
    return dct

def get_grouped_test_details(user_id, test_id_list, question_group_dct):
    from utils.connect_db import get_db_connection

    conn = None
    cur = None
    try:
        conn = get_db_connection()
        if not conn:
            return []

        cur = conn.cursor()

        # クエリ用のIN句プレースホルダ
        test_id_placeholders = ','.join(['%s'] * len(test_id_list))
        sql = f"""
            SELECT test_id, question_detail_id
            FROM test_details
            WHERE user_id = %s AND test_id IN ({test_id_placeholders})
        """
        cur.execute(sql, [user_id] + test_id_list)
        rows = cur.fetchall()

        # question_detail_id から group_id を逆引きできる辞書を構築
        qd_to_group = {}
        for group_id, qd_list in question_group_dct.items():
            for qd_id in qd_list:
                qd_to_group[qd_id] = group_id

        result = []
        for test_id, qd_id in rows:
            group_id = qd_to_group.get(qd_id)
            if group_id is not None:
                result.append((test_id, qd_id, group_id))

        return result
    except Exception as e:
        print(f"エラー: {e}")
        return []
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


from collections import defaultdict

def group_by_group_id(client_test_data):
    grouped = defaultdict(list)
    for test_id, question_detail_id, group_id in client_test_data:
        grouped[group_id].append((test_id, question_detail_id))

    result = {}
    for group_id, items in grouped.items():
        # test_id でソート
        items.sort(key=lambda x: x[0])
        # question_detail_id のリストだけ抽出
        question_detail_ids = [qd_id for _, qd_id in items]
        result[group_id] = question_detail_ids

    return result

from sklearn.metrics import cohen_kappa_score

import numpy as np

def calculate_qwk(y_true, y_pred):
    """
    2つのリスト y_true, y_pred を受け取り、
    Quadratic Weighted Kappa (QWK) を返す。
    """
    if len(y_true) != len(y_pred):
        raise ValueError("リストの長さが一致しません。")
    
    # すべてのラベルが同じ（片方または両方）の場合の処理
    if len(set(y_true)) == 1 and len(set(y_pred)) == 1:
        if y_true == y_pred:
            return 1.0  # 完全一致
        else:
            return 0.0  # ラベルが一種類ずつだが一致していない
    
    qwk_score = cohen_kappa_score(y_true, y_pred, weights='quadratic')

    # NaNが出る場合があるのでチェック
    if np.isnan(qwk_score):
        return 0.0

    return qwk_score

from utils.connect_db import get_db_connection

def delete_test_details_by_user_and_tests(user_id, test_ids):
    """
    指定した user_id と test_id のリストに一致する test_details の行をすべて削除します。
    """
    if not test_ids:
        print("削除対象の test_id が空です。")
        return False

    conn = None
    cur = None
    try:
        conn = get_db_connection()
        if not conn:
            return False

        cur = conn.cursor()
        
        # IN 句のパラメータを安全に作成
        sql = f"""
            DELETE FROM test_details
            WHERE user_id = %s AND test_id = ANY(%s)
        """
        cur.execute(sql, (user_id, test_ids))

        conn.commit()
        print(f"{cur.rowcount} 件の test_details を削除しました。")
        return True

    except Exception as e:
        print(f"test_details 削除中にエラーが発生しました: {e}")
        if conn:
            conn.rollback()
        return False

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
