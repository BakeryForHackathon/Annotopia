from utils.connect_db import get_db_connection

def make_test_data(user_id, test_data_id, answers):
    """
    指定された user_id と test_data_id に対応する test_details 行を取得し、
    answers に基づいて question_detail_id を更新します。
    
    answers: question_detail_id のリスト
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
            SELECT id FROM test_details
            WHERE user_id = %s AND test_id = %s
            ORDER BY id ASC
        """, (user_id, test_data_id))
        rows = cur.fetchall()
        
        if len(rows) != len(answers):
            print("エラー: 回答数が既存のテスト詳細数と一致しません。")
            return False
        
        # 1件ずつ update する
        for i, row in enumerate(rows):
            test_detail_id = row[0]
            question_detail_id = answers[i]
            cur.execute("""
                UPDATE test_details
                SET question_detail_id = %s
                WHERE id = %s
            """, (question_detail_id, test_detail_id))
        
        conn.commit()
        return True

    except Exception as e:
        print(f"make_test_data 実行中にエラーが発生しました: {e}")
        if conn:
            conn.rollback()
        return False

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
