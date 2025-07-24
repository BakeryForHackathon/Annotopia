from utils.connect_db import get_db_connection

def get_ids_by_task_id(task_id, table_name):
    """
    指定されたテーブルから、task_id に一致する全ての id をリストで返す。

    Parameters:
        task_id (int): 検索対象の task_id
        table_name (str): 対象テーブル名（安全な固定名のみを受け入れること）

    Returns:
        list[int] または None（エラー時）
    """
    # セキュリティ上、許可するテーブル名のみホワイトリストで制限する
    allowed_tables = {"questions", "test_data", "annotation_data"}
    if table_name not in allowed_tables:
        raise ValueError(f"不正なテーブル名が指定されました: {table_name}")

    conn = None
    cur = None
    try:
        conn = get_db_connection()
        if not conn:
            return None

        cur = conn.cursor()

        # SQL構文は task_id によるフィルタと id の取得
        query = f"SELECT id FROM {table_name} WHERE task_id = %s"
        cur.execute(query, (task_id,))
        results = cur.fetchall()

        return [row[0] for row in results]
    except Exception as e:
        print(f"{table_name} テーブルのID取得中にエラー: {e}")
        return None
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
