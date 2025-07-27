from utils.connect_db import get_db_connection

def get_user_annotation_count(user_id,task_id):
    """
    指定された task_id に対応する annotation_data のうち、
    user_id がアノテーションしたユニークな annotation_id の件数を返す。
    """
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        if not conn:
            return None

        cur = conn.cursor()
        cur.execute("""
            SELECT COUNT(DISTINCT ad.id)
            FROM annotation_data ad
            JOIN annotation_details atd ON ad.id = atd.annotation_id
            WHERE ad.task_id = %s AND atd.user_id = %s
        """, (task_id, user_id))
        
        count = cur.fetchone()[0]
        return count

    except Exception as e:
        print(f"重複なし注釈件数の取得中にエラーが発生しました: {e}")
        return None

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
