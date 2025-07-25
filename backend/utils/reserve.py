from utils.connect_db import get_db_connection 
from datetime import datetime, timedelta, timezone

def reserve_annotation(user_id, task_id, annotation_data_id):
    """
    予約を5分間登録する。既に同一データが予約済みなら何もしない。
    成功時: True, 予約済みなどで挿入できなかった場合: False
    """
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        if not conn:
            return False

        cur = conn.cursor()

        now = datetime.now(timezone.utc)
        expires_at = now + timedelta(minutes=5)

        cur.execute("""
            INSERT INTO reservations (task_id, annotation_data_id, user_id, start_time, expires_at)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (annotation_data_id) DO NOTHING
            RETURNING id
        """, (task_id, annotation_data_id, user_id, now, expires_at))

        inserted = cur.fetchone()
        conn.commit()

        return inserted is not None

    except Exception as e:
        print(f"予約処理中にエラーが発生しました: {e}")
        if conn:
            conn.rollback()
        return False
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
