from utils.connect_db import get_db_connection
from datetime import datetime, timezone

def clean_reservations(user_id):
    """
    現在の時間を基にして、次の2種類の予約データを削除する:
    1. 現在時刻が expires_at を超えている行（期限切れ予約）
    2. user_id に一致する予約行（ユーザーによるキャンセルなど）
    """
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        if not conn:
            return False

        cur = conn.cursor()
        
        # 現在のUTC時刻（推奨スタイル）
        now = datetime.now(timezone.utc)

        # 1. 有効期限を過ぎた予約を削除
        cur.execute("""
            DELETE FROM reservations
            WHERE expires_at IS NOT NULL AND expires_at < %s
        """, (now,))
        
        # 2. 自分の予約を削除
        cur.execute("""
            DELETE FROM reservations
            WHERE user_id = %s
        """, (user_id,))
        
        conn.commit()
        return True
    except Exception as e:
        print(f"予約のクリーンアップ中にエラーが発生しました: {e}")
        if conn:
            conn.rollback()
        return False
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
