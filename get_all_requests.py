from utils.connect_db import get_db_connection

def get_all_requests(user_id):
    """
    tasks テーブルに存在するすべてのタスクを取得し、
    タスクID・タイトル・進捗率・開始日・終了日を含む辞書を返す。
    """
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        if not conn:
            return None

        cur = conn.cursor()
        query = """
            SELECT 
                id, title, description, start_day, end_day, max_annotations_per_user
            FROM 
                tasks
        """
        cur.execute(query)
        rows = cur.fetchall()

        task_list = []
        for row in rows:
            task_id, title, description, start_day, end_day, max_annotations_per_user = row
            

            task_list.append({
                "task_id": task_id,
                "title": title,
                "description": description,
                "annotation_count": max_annotations_per_user,
                "created_at": start_day.strftime("%Y-%m-%d") if start_day else None,
                "due_date": end_day.strftime("%Y-%m-%d") if end_day else None
            })

        return { 
            "user_id": user_id,
            "tasks": task_list
        }

    except Exception as e:
        print(f"タスク取得中にエラーが発生しました: {e}")
        return None
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
