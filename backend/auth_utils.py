# auth_utils.py

"""
ユーザー認証を行う関数
"""
from utils.connect_db import get_db_connection

# 認証エラー用のカスタム例外を定義
class AuthError(Exception):
    pass

def authenticate_user(name, password):
    """
    認証に失敗した場合、AuthErrorを発生させます。
    """
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        if not conn:
            raise AuthError("データベース接続に失敗しました。接続設定を確認してください。")

        cur = conn.cursor()
        cur.execute("SELECT id, name, password FROM users WHERE name = %s", (name,))
        user_record = cur.fetchone()

        if user_record:
            user_id, db_name, db_password = user_record
            if password == db_password:
                # 認証成功
                return {"id": user_id, "name": db_name}
            else:
                # パスワード不一致
                raise AuthError("パスワードが一致しません。")
        else:
            # ユーザーが見つからない
            raise AuthError(f"ユーザー '{name}' はデータベースに存在しません。")

    except AuthError:
        # 自分で定義した認証エラーはそのまま上に投げる
        raise
    except Exception as e:
        # その他の予期せぬエラー
        raise AuthError(f"認証処理中に予期せぬエラーが発生しました: {e}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()