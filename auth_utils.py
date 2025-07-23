"""
ユーザー認証を行う関数
"""

from utils.connect_db import get_db_connection
    
def authenticate_user(username, password):
    """
    提供されたユーザー名とパスワードでユーザーを認証します。
    PostgreSQLデータベースの'users'テーブルを参照します。
    認証に成功した場合、ユーザー辞書を返します。それ以外の場合はNoneを返します。
    """
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        if not conn:
            return None

        cur = conn.cursor()
        
        # ユーザー名でユーザー情報を検索
        # 実際には、パスワードはハッシュ化された状態でDBに保存し、
        # check_password_hash(stored_hash, input_password) のように比較します。
        cur.execute("SELECT id, username, password FROM users WHERE username = %s", (username,))
        user_record = cur.fetchone()

        if user_record:
            user_id, db_username, db_password = user_record
            
            # ここでパスワードを比較します。
            # 本番環境では、check_password_hash(db_password, password) を使用してください。
            if password == db_password: # 平文パスワードの比較 (非推奨)
            # if check_password_hash(db_password, password): # ハッシュ化パスワードの比較 (推奨)
                return {
                    "id": user_id,
                    "username": db_username,
                }
        return None
    except Exception as e:
        print(f"認証処理中にエラーが発生しました: {e}")
        return None
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()