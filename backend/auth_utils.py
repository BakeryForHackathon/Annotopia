"""
ユーザー認証を行う関数
"""
from utils.connect_db import get_db_connection 
    
def authenticate_user(name, password):
    """
    提供されたユーザー名とパスワードでユーザーを認証します。
    PostgreSQLデータベースの'users'テーブルを参照します。
    認証に成功した場合、ユーザー辞書を返します。それ以外の場合はNoneを返します。
    """
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        if conn == 0:
            return 1
        else if not conn:
            return 0
            # return None

        cur = conn.cursor()
        
        # ユーザー名でユーザー情報を検索
        cur.execute("SELECT id, name, password FROM users WHERE name = %s", (name,))
        user_record = cur.fetchone()

        if user_record:
            user_id, db_name, db_password = user_record

            # パスワードの比較
            if password == db_password:  # 平文パスワードの比較 (非推奨)
            # if check_password_hash(db_password, password):  # ハッシュ化パスワードの比較 (推奨)
                return {
                    "id": user_id,
                    "name": db_name,
                }
        return 2
        # return None
    except Exception as e:
        print(f"認証処理中にエラーが発生しました: {e}")
        return 3
        # return None
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
