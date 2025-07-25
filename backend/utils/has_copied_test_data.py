from utils.connect_db import get_db_connection

def has_copied_test_data_any(user_id, task_id):
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        if not conn:
            return False

        cur = conn.cursor()
        cur.execute("""
            SELECT 1 FROM test_details td
            JOIN test_data t ON td.test_id = t.id
            WHERE td.user_id = %s AND t.task_id = %s
            LIMIT 1
        """, (user_id, task_id))
        return cur.fetchone() is not None

    except Exception as e:
        print(f"コピー済み{e}")
        return False
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
