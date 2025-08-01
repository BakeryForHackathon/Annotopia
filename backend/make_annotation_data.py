from utils.connect_db import get_db_connection
from clean_reservations import clean_reservations
from utils.get_randam_annotation_id import get_unanswered_annotation_ids
def make_annotation_data(user_id, annotation_data_id, answers):
    """
    指定された annotation_data_id に対応する annotation_details 行を取得し、
    answers に基づいて question_detail_id と user_id を更新します。
    
    answers: True または False
    """
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        if not conn:
            return False

        cur = conn.cursor()
        
        # 指定の user_id と test_id に一致する test_details の行を取得
        cur.execute("""
            SELECT id FROM annotation_details
            WHERE annotation_id = %s
            ORDER BY id ASC
        """, (annotation_data_id,))
        rows = cur.fetchall()
        
        if len(rows) != len(answers):
            print("エラー: 回答数が既存のテスト詳細数と一致しません。")
            return False
        
        # 1件ずつ update する
        for i, row in enumerate(rows):
            annotation_detail_id = row[0]
            question_detail_id = answers[i]
            cur.execute("""
                UPDATE annotation_details
                SET question_detail_id = %s,
                    user_id = %s
                WHERE id = %s
            """, (question_detail_id, user_id, annotation_detail_id))

        # === task_id を取得する ===
        cur.execute("""
            SELECT task_id FROM annotation_data
            WHERE id = %s
        """, (annotation_data_id,))
        result = cur.fetchone()
        if not result:
            print("annotation_data_id に対応する task_id が見つかりません。")
            return False
        task_id = result[0]

        # === tasks テーブルの情報取得 ===
        cur.execute("""
            SELECT total_data_count FROM tasks
            WHERE id = %s
        """, (task_id,))
        result = cur.fetchone()
        if not result:
            print("task_id に対応するタスクが見つかりません。")
            return False
        total_data_count = result[0]

        # === 未回答の annotation_data の数を取得 ===
        unanswered_annotation_ids = get_unanswered_annotation_ids(task_id)
        unanswered_count = len(unanswered_annotation_ids) if unanswered_annotation_ids is not None else 0

        # === annotated_data_count を再計算して更新 ===
        new_annotated_count = total_data_count - unanswered_count +1
        if new_annotated_count < 0:
            new_annotated_count = 0  # 念のためマイナスを防ぐ

        cur.execute("""
            UPDATE tasks
            SET annotated_data_count = %s
            WHERE id = %s
        """, (new_annotated_count, task_id))

        
        conn.commit()
        clean_reservations(user_id)
        return True

    except Exception as e:
        print(f"make_annotation_data 実行中にエラーが発生しました: {e}")
        if conn:
            conn.rollback()
        return False

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
