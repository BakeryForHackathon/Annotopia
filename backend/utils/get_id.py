from utils.connect_db import get_db_connection

def get_client_id_by_task(task_id):
    """
    指定された task_id に対応する tasks テーブルの client_id を返す。
    見つからなければ None を返す。
    """
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        if not conn:
            return None

        cur = conn.cursor()
        cur.execute("SELECT client_id FROM tasks WHERE id = %s", (task_id,))
        result = cur.fetchone()

        if result:
            return result[0]  # client_id を返す
        else:
            return None
    except Exception as e:
        print(f"client_id の取得中にエラーが発生しました: {e}")
        return None
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

from utils.connect_db import get_db_connection

def get_threshold_by_task_id(task_id):
    """
    task_id に対応する tasks テーブルの threshold を返す。
    見つからなければ None を返す。
    """
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        if not conn:
            return None

        cur = conn.cursor()
        cur.execute("SELECT threshold FROM tasks WHERE id = %s", (task_id,))
        result = cur.fetchone()

        if result:
            return float(result[0]) if result[0] is not None else None
        else:
            return None
    except Exception as e:
        print(f"threshold の取得中にエラーが発生しました: {e}")
        return None
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()