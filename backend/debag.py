from utils.connect_db import get_db_connection

def fetch_all_from_table(table_name):
    """
    指定したテーブルの全データを取得してリストで返す。
    table_nameはSQLインジェクション対策のため、ホワイトリストでチェック推奨。
    """
    # セキュリティのため許可テーブル名だけ受け付ける例
    allowed_tables = {
        "users", "tasks", "questions", "question_details",
        "test_data", "test_details", "annotation_data", "annotation_details"
    }

    if table_name not in allowed_tables:
        raise ValueError(f"許可されていないテーブル名です: {table_name}")

    conn = None
    cur = None
    try:
        conn = get_db_connection()
        if not conn:
            print("DB接続失敗")
            return None
        
        cur = conn.cursor()

        # カラム名も一緒に取得
        cur.execute(f"SELECT * FROM {table_name}")
        rows = cur.fetchall()
        colnames = [desc[0] for desc in cur.description]

        # 辞書のリストに変換
        results = [dict(zip(colnames, row)) for row in rows]

        return results

    except Exception as e:
        print(f"{table_name} 取得中にエラー発生: {e}")
        return None

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
