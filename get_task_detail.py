from utils.connect_db import get_db_connection
from utils.get_requests import get_questions_by_task
from utils.is_ended import is_test_ended
def get_task_detail(user_id, task_id):
    """
    指定された user_id と task_id に対するタスクの詳細情報を取得して返す。
    questions, ended は未実装。
    """
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        if not conn:
            return None

        cur = conn.cursor()

        # tasksテーブルからタスク基本情報を取得
        query = """
            SELECT 
                title, description, start_day, end_day, max_annotations_per_user
            FROM 
                tasks
            WHERE 
                id = %s
        """
        cur.execute(query, (task_id,))
        row = cur.fetchone()

        if row is None:
            return None  # 指定された task_id が存在しない

        title, description, start_day, end_day, max_annotations_per_user = row

        ended = is_test_ended(user_id, task_id)
        questions = get_questions_by_task(task_id)
        # タスク詳細情報を構成（questionsなどは後ほど追加）
        task_detail = {
            "user_id": user_id,
            "task_id": task_id,
            "title": title,
            "description": description,
            "question_count": len(questions),      # 仮で0（後で変更）
            "questions": questions,         # 仮で空リスト（後で変更）
            "start_day": start_day.strftime("%Y/%m/%d") if start_day else None,
            "end_day": end_day.strftime("%Y/%m/%d") if end_day else None,
            "max_annotations_per_user": max_annotations_per_user,
            "ended": ended            # 未定義
        }

        return task_detail

    except Exception as e:
        print(f"タスク詳細取得中にエラーが発生しました: {e}")
        return None
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
