from utils.get_requests import get_questions_by_task

def get_task_annotated_data(task_id):
    print()
    requests = get_questions_by_task(task_id)

    dct = get_annotation_data_with_answers(task_id)
    annotated_df = convert_to_dataframe(dct, requests)

    return annotated_df



from utils.connect_db import get_db_connection

def get_annotation_data_with_answers(task_id):
    """
    指定された task_id に紐づく annotation_data と annotation_details を結合し、
    annotation_id ごとに {data, answers} の辞書形式で返す。
    """
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        if not conn:
            return None

        cur = conn.cursor()

        # JOINで annotation_data と annotation_details を取得
        cur.execute("""
            SELECT 
                ad.id AS annotation_id,
                ad.data,
                atd.question_detail_id,
                atd.user_id
            FROM annotation_data ad
            LEFT JOIN annotation_details atd ON ad.id = atd.annotation_id
            WHERE ad.task_id = %s
            ORDER BY ad.id
        """, (task_id,))
        
        rows = cur.fetchall()

        # 構造構築
        result = {}
        for annotation_id, data, question_detail_id, user_id in rows:
            if annotation_id not in result:
                result[annotation_id] = {
                    "data": data,
                    "answers": []
                }
            if question_detail_id is not None and user_id is not None:
                result[annotation_id]["answers"].append({
                    "question_detail_id": question_detail_id,
                    "user_id": user_id
                })

        return result

    except Exception as e:
        print(f"データ取得中にエラーが発生しました: {e}")
        return None

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


    
import pandas as pd

def convert_to_dataframe(dct, requests):
    # 1. requests から {question_detail_id: (question, scale)} 辞書を作る
    detail_id_to_question_scale = {}
    for item in requests:
        question = item["question"]
        for detail in item["details"]:
            qd_id = detail["question_details_id"]
            scale = detail["scale"]
            detail_id_to_question_scale[qd_id] = (question, scale)

    # 2. 結果格納用リスト
    rows = []

    # 3. dctをannotation_id（key）で昇順ソートして処理
    for annotation_id in sorted(dct.keys()):
        entry = dct[annotation_id]
        data_value = entry["data"]
        answers = entry["answers"]

        # 複数のユーザー回答がある場合は1件ずつ処理
        for ans in answers:
            row = {
                "id": annotation_id,
                "data": data_value,
                "user_id": ans["user_id"]
            }

            qd_id = ans["question_detail_id"]
            question_info = detail_id_to_question_scale.get(qd_id)
            if question_info:
                question, scale = question_info
                row[question] = scale  # 質問名を列名として使う

            rows.append(row)

    # 4. DataFrame に変換（列が揃うよう自動補完）
    df = pd.DataFrame(rows)

    return df