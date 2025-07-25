from utils.get_user_annotation_count import get_user_annotation_count
from utils.connect_db import get_db_connection

def is_annotation_ended(user_id, task_id):
    """
    指定された user_id, task_id のユーザーが注釈を終了しているか（全件注釈済みか）を判定。
    注釈数 == max_annotations_per_user なら True、それ以外は False を返す。
    """
    answered_ids = get_user_annotation_count(user_id, task_id)

    conn = None
    cur = None
    try:
        conn = get_db_connection()
        if not conn:
            return False  # 接続失敗時は False 扱い

        cur = conn.cursor()
        cur.execute("SELECT max_annotations_per_user FROM tasks WHERE id = %s", (task_id,))
        row = cur.fetchone()

        if row is None or row[0] is None:
            print("max_annotations_per_user が取得できませんでした。")
            return False

        max_annotations = row[0]
        return answered_ids >= max_annotations

    except Exception as e:
        print(f"注釈終了判定中にエラーが発生しました: {e}")
        return False

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()