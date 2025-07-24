from utils.connect_db import get_db_connection

def set_annotation_data(annotation_ids, count):
    """
    annotation_idsの各要素に対して、count個ずつ annotation_details にレコードを挿入します。
    user_id、question_detail_id は NULL とします。
    """
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        if not conn:
            return False

        cur = conn.cursor()
        insert_query = """
            INSERT INTO annotation_details (annotation_id, question_detail_id, user_id)
            VALUES (%s, %s, %s)
        """

        for annotation_id in annotation_ids:
            for _ in range(count):
                cur.execute(insert_query, (annotation_id, None, None))

        conn.commit()
        return True
    except Exception as e:
        print(f"annotation_details挿入中にエラーが発生しました: {e}")
        if conn:
            conn.rollback()
        return False
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()