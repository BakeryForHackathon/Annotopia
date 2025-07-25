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
    print("--- 認証処理開始 ---")
    print(f"入力ユーザー名: {name}") # 入力されたユーザー名を確認

    conn = None
    cur = None
    try:
        conn = get_db_connection()
        if not conn:
            # 接続失敗のログ
            print("★★★ エラー: データベース接続に失敗しました。接続設定を確認してください。")
            return None
        
        print("データベース接続成功。")
        cur = conn.cursor()
        
        # ユーザー名でユーザー情報を検索
        cur.execute("SELECT id, name, password FROM users WHERE name = %s", (name,))
        user_record = cur.fetchone()

        if user_record:
            print(f"ユーザーが見つかりました: {user_record}")
            user_id, db_name, db_password = user_record

            # パスワードの比較
            if password == db_password:
                print("パスワードが一致しました。認証成功。")
                return {
                    "id": user_id,
                    "name": db_name,
                }
            else:
                # パスワード不一致のログ
                print("★★★ エラー: パスワードが一致しません。")
                print(f"入力されたパスワード: '{password}'")
                print(f"データベースのパスワード: '{db_password}'")
                return None
        else:
            # ユーザー不在のログ
            print(f"★★★ エラー: ユーザー '{name}' はデータベースに見つかりませんでした。")
            return None
            
    except Exception as e:
        print(f"★★★ 認証処理中に予期せぬエラーが発生しました: {e}")
        return None
    finally:
        print("--- 認証処理終了 ---")
        if cur:
            cur.close()
        if conn:
            conn.close()