from utils.connect_db import get_db_connection

def get_unanswered_annotation_ids(task_id):
    """
    指定した task_id の annotation_data のうち、
    annotation_details で question_detail_id が NULL の annotation_id のリストを返す。
    エラー時は None を返す。
    """
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        if not conn:
            return None

        cur = conn.cursor()
        query = """
            SELECT DISTINCT ad.id
            FROM annotation_data ad
            LEFT JOIN annotation_details atd ON ad.id = atd.annotation_id
            WHERE ad.task_id = %s
              AND (atd.question_detail_id IS NULL OR atd.question_detail_id IS NULL)
        """
        cur.execute(query, (task_id,))
        rows = cur.fetchall()
        return [row[0] for row in rows]

    except Exception as e:
        print(f"未回答のannotation_id取得中にエラーが発生しました: {e}")
        return None
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def get_reversed_annotation_ids(task_id):
    """
    指定された task_id に紐づく reservations テーブルの annotation_data_id のリストを返す。
    """
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        if not conn:
            return None

        cur = conn.cursor()
        cur.execute("""
            SELECT annotation_data_id
            FROM reservations
            WHERE task_id = %s
        """, (task_id,))
        rows = cur.fetchall()
        
        # annotation_data_id のリストを返す
        return [row[0] for row in rows] if rows else []
    except Exception as e:
        print(f"予約情報の取得中にエラーが発生しました: {e}")
        return None
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def get_available_unanswered_annotation_ids(task_id):
    """
    指定された task_id に対して、question_detail_id が NULL であり、
    reservations に登録されていない annotation_data_id のリストを返す。
    エラー時は None を返す。
    """
    try:
        # 未回答の annotation_id を取得
        unanswered_ids = get_unanswered_annotation_ids(task_id)
        if unanswered_ids is None:
            return None
        
        # 予約済みの annotation_data_id を取得
        reserved_ids = get_reversed_annotation_ids(task_id)
        if reserved_ids is None:
            return None
        
        # 未回答かつ予約されていない ID を抽出
        available_ids = [aid for aid in unanswered_ids if aid not in reserved_ids]
        return available_ids
    
    except Exception as e:
        print(f"利用可能な未回答 annotation_id の取得中にエラーが発生しました: {e}")
        return None
    
import random

def select_random_unanswered_annotation(task_id):
    """
    ユーザーがまだ回答していない annotation_data の中からランダムに 1 件の test_id を選んで返す。
    """
    unanswered_ids = get_available_unanswered_annotation_ids(task_id)
    if not unanswered_ids:
        print("未回答のアノテーションデータはありません。")
        return None

    return random.choice(unanswered_ids)
