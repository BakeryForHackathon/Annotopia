from utils.connect_db import get_db_connection


def set_test_data(test_ids, user_id, count):
    """
    test_idsの各要素に対して、count個ずつ test_details にレコードを挿入します。
    user_id はすべて共通、question_detail_id は NULL とします。
    
    例:
        test_ids = [1, 2]
        user_id = 99
        count = 3

        => test_details に 6行挿入（test_id=1が3行、test_id=2が3行）
    """
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        if not conn:
            return False

        cur = conn.cursor()
        insert_query = """
            INSERT INTO test_details (test_id, question_detail_id, user_id)
            VALUES (%s, NULL, %s)
        """

        for test_id in test_ids:
            for _ in range(count):
                cur.execute(insert_query, (test_id, user_id))

        conn.commit()
        return True
    except Exception as e:
        print(f"test_details挿入中にエラーが発生しました: {e}")
        if conn:
            conn.rollback()
        return False
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()