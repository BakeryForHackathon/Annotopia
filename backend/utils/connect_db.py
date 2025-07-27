import os
import psycopg2

def get_db_connection():
    """
    PostgreSQLデータベースへの接続を確立し、接続オブジェクトを返します。
    接続情報は環境変数から取得します。
    """
    try:
        conn = psycopg2.connect(
            host=os.environ.get('DB_HOST', 'localhost'),
            database=os.environ.get('DB_NAME', 'your_database_name'),
            user=os.environ.get('DB_USER', 'your_username'),
            password=os.environ.get('DB_PASSWORD', 'your_password'),
            port=os.environ.get('DB_PORT', '5432')
        )
        return conn
    except Exception as e:
        print(f"データベース接続エラー: {e}")
        return 0