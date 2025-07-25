"""
画面遷移時にannotationデータを取得するためのコードを記述します。
dct = get_annotation_data(user_name, task_id) 
dct = {
  “user_id”
  “task_id”
   “annotation_data_id”
   “data”:原文: She went to the store to buy some milk.\n訳文: 彼女はミルクを買うために店に行った。
    “data_count” 0                   ←annotate済みのデータ数　　+1して問1にする
    status:”20%”
    questions : [
        {
             question:正確さ
             scale:
             scale_discription:[
                 原文の意味をほとんどまたは全く伝えていない。意味が通らないか、全く異なる内容になっている。,
                 原文の意味の半分以上は伝えているが、重要な情報の抜けや軽微な誤訳がある。,
                 原文の意味を完全に伝えており、情報の欠落や誤訳がまったくない。                  
             ]
     }
}
"""
import random
import time
from utils.reserve import reserve_annotation
from utils.get_randam_annotation_id import get_available_unanswered_annotation_ids
from utils.get_user_annotation_count import get_user_annotation_count
from utils.get_requests import get_questions_by_task
import random
import time
from utils.connect_db import get_db_connection
from clean_reservations import clean_reservations

def get_annotation_data(user_id, task_id):
    """
    ユーザーがまだ回答しておらず予約されていない annotation_data をランダムに1つ予約し、
    指定形式の辞書を返す。
    """
    tried = set()

    while True:
        unanswered_ids = get_available_unanswered_annotation_ids(task_id)
        if not unanswered_ids:
            print("未回答で予約されていないアノテーションデータは存在しません。")
            return None

        candidates = [aid for aid in unanswered_ids if aid not in tried]
        if not candidates:
            print("すべての候補に対して予約を試みましたが、予約できませんでした。")
            return None

        annotation_data_id = random.choice(candidates)
        tried.add(annotation_data_id)

        clean_reservations(user_id)
        success = reserve_annotation(user_id, task_id, annotation_data_id)
        
        if success:
            print(f"✅ annotation_data_id={annotation_data_id} を予約しました。")

            # --- データ構築 ---
            conn = get_db_connection()
            cur = conn.cursor()

            # annotation_data の data を取得
            cur.execute("SELECT data FROM annotation_data WHERE id = %s", (annotation_data_id,))
            row = cur.fetchone()
            data_text = row[0] if row else ""

            # data_count を取得
            data_count = get_user_annotation_count(user_id, task_id)

            # max_annotations_per_user を取得
            cur.execute("SELECT max_annotations_per_user FROM tasks WHERE id = %s", (task_id,))
            row = cur.fetchone()
            max_annotations = row[0] if row and row[0] else 1  # ゼロ除算防止

            # ステータス（割合）を計算
            status_percent = round((data_count) / max_annotations * 100)
            status_str = f"{status_percent}%"

            # 質問リストを取得
            questions = get_questions_by_task(task_id)

            cur.close()
            conn.close()

            # 辞書形式で返す
            dct = {
                "user_id": user_id,
                "task_id": task_id,
                "annotation_data_id": annotation_data_id,
                "data": data_text,
                "data_count": data_count,  # 1から始めたいなら +1
                "status": status_str,
                "questions": questions
            }

            return dct

        else:
            print(f"annotation_data_id={annotation_data_id} の予約に失敗。他を試します...")
            time.sleep(0.5)



