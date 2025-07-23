"""
発注済み依頼リストを返す関数
"""

from utils.connect_db import get_db_connection
from psycopg2.extras import RealDictCursor

def get_requests(user_id):
    """
    提供されたユーザーIDに基づいて、関連するタスク情報を取得します。
    PostgreSQLデータベースの'tasks'テーブルを参照します。
    ユーザーIDに関連するタスク情報を含む辞書を返します。
    """
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        if not conn:
            return None

        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        # ユーザー名でユーザー情報を検索
        # 実際には、パスワードはハッシュ化された状態でDBに保存し、
        # check_password_hash(stored_hash, input_password) のように比較します。
        cur.execute("""
                    SELECT 
                        id AS task_id,
                        title, 
                        total_data_count, 
                        annotated_data_count,
                        start_day AS created_at,
                        end_day AS due_date
                    FROM tasks 
                    WHERE client_id = %s
                    ORDER BY created_at DESC
                """, (user_id,))
        tasks_from_db = cur.fetchall()
        formatted_tasks = []
        for task in tasks_from_db:
            # created_at (TIMESTAMPTZ) を 'YYYY-MM-DD' 形式の文字列に変換
            task['created_at'] = task['created_at'].strftime('%Y-%m-%d')
            # due_date (DATE) を 'YYYY-MM-DD' 形式の文字列に変換
            if task['total_data_count'] > 0:
                progress = task['annotated_data_count'] / task['total_data_count']
            else:
                progress = 0.0
            
            # 進捗率を status に代入（例：'65%'）
            task['status'] = f"{round(progress * 100)}%"

            formatted_tasks.append(task)

        # 最終的なJSON構造を作成
        result = {
            "user_id": user_id,
            "tasks": formatted_tasks
        }

        return result

    except Exception as e:
        print(f"API用タスクデータ取得中にエラーが発生しました: {e}")
        return None
    finally:
        if conn:
            conn.close()