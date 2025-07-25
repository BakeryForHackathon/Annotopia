from utils.connect_db import get_db_connection

def get_test_detail_pairs(user_id, test_ids):
    """
    指定された user_id および test_ids リストに一致する
    test_details テーブルの (test_id, question_detail_id) のペアを返す。
    
    引数:
        user_id (int): 対象ユーザーID
        test_ids (List[int]): 検索対象の test_id のリスト

    戻り値:
        List[Tuple[int, int]]: (test_id, question_detail_id) のペアのリスト
    """
    if not test_ids:
        return []

    conn = None
    cur = None
    try:
        conn = get_db_connection()
        if not conn:
            return []

        cur = conn.cursor()

        # プレースホルダを test_ids の数に合わせて生成
        placeholders = ','.join(['%s'] * len(test_ids))
        query = f"""
            SELECT test_id, question_detail_id
            FROM test_details
            WHERE user_id = %s
            AND test_id IN ({placeholders})
        """
        params = [user_id] + test_ids
        cur.execute(query, params)
        results = cur.fetchall()

        return results  # List[Tuple[test_id, question_detail_id]]

    except Exception as e:
        print(f"test_details の取得中にエラーが発生しました: {e}")
        return []
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
