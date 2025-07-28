from utils.connect_db import get_db_connection

def sign_up_user(user_name, user_password):
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        if not conn:
            return None

        cur = conn.cursor()

        # ユーザー情報を挿入して、挿入されたIDを返す
        insert_query = """
            INSERT INTO users (name, password)
            VALUES (%s, %s)
            RETURNING id;
        """
        cur.execute(insert_query, (user_name, user_password))
        user_id = cur.fetchone()[0]
        conn.commit()

        return user_id

    except Exception as e:
        print(f"ユーザー登録中にエラーが発生しました: {e}")
        return None
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
