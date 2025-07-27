"""
タスクidを引数にして
questionを辞書形式で返す関数
"""
from utils.connect_db import get_db_connection
from collections import defaultdict
def get_questions_by_task(task_id):
    """
    指定された task_id に紐づく質問とそのスケール情報を取得し、
    以下のような構造のリストとして返す：

    [
        {
          "details": [
            {
              "question_details_id": 3,
              "scale": 3,
              "scale_description": "原文の意味を完全に伝えており、情報の欠落や誤訳がまったくない。"
            },
            {
              "question_details_id": 2,
              "scale": 2,
              "scale_description": "原文の意味の半分以上は伝えているが、重要な情報の抜けや軽微な誤訳がある。"
            },
            {
              "question_details_id": 1,
              "scale": 1,
              "scale_description": "原文の意味をほとんどまたは全く伝えていない。"
            }
          ],
          "question": "正確さ"
        },
        {
          "details": [
            {
              "question_details_id": 5,
              "scale": 2,
              "scale_description": "全然ダメ"
            },
            {
              "question_details_id": 4,
              "scale": 1,
              "scale_description": "いい感じ"
            }
          ],
          "question": "流暢性"
        }
      ],

    """
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        if not conn:
            return None

        cur = conn.cursor()

        cur.execute("""
            SELECT q.id, q.title, qd.id, qd.scale, qd.description
            FROM questions q
            JOIN question_details qd ON q.id = qd.question_id
            WHERE q.task_id = %s
            ORDER BY q.id, qd.scale DESC
        """, (task_id,))
        rows = cur.fetchall()

        if not rows:
            return []

        question_map = defaultdict(lambda: {"question": "", "details": []})

        for q_id, q_title, qd_id, scale, description in rows:
            question_map[q_id]["question"] = q_title
            try:
                scale_val = int(scale)
            except:
                scale_val = scale
            question_map[q_id]["details"].append({
                "question_details_id": qd_id,
                "scale": scale_val,
                "scale_description": description
            })

        return list(question_map.values())

    except Exception as e:
        print(f"質問詳細の取得中にエラーが発生しました: {e}")
        return None
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()