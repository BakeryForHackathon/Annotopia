"""
タスクの作成画面でボタン押下時に内容を保存する関数
"""
from utils.connect_db import get_db_connection
from utils.get_ids import get_ids_by_task_id
from utils.set_test_data import set_test_data
from utils.set_annotation_data import set_annotation_data

def create_task(task_dict):
    import psycopg2
    import pandas as pd
    
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        if not conn:
            print("DB接続失敗")
            return False
        conn.set_client_encoding('UTF8')
        cur = conn.cursor()

        # 1. tasks テーブルに保存
        cur.execute("""
            INSERT INTO tasks (
                client_id, title, description, private,
                start_day, end_day, total_data_count,
                annotated_data_count, total_test_data_count,
                max_annotations_per_user, test, threshold
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (
            task_dict["user_id"],
            task_dict["title"],
            task_dict["description"],
            task_dict["private"],
            task_dict["start_day"],
            task_dict["end_day"],
            len(task_dict["data"]),
            0,
            len(task_dict["test_data"]),
            task_dict["max_annotations_per_user"],
            task_dict["test"],
            task_dict["threshold"]
        ))
        task_id = cur.fetchone()[0]

        # 2. questions テーブルに保存
        for q in task_dict["questions"]:
            cur.execute("""
                INSERT INTO questions (task_id, title)
                VALUES (%s, %s)
                RETURNING id
            """, (task_id, q["question"]))
            question_id = cur.fetchone()[0]

            # 3. question_details テーブルに scale を保存
            for idx,scale_text in enumerate(q["scale_discription"]):
                cur.execute("""
                    INSERT INTO question_details (question_id, description, scale)
                    VALUES (%s, %s, %s)
                """, (question_id, scale_text, idx+1))  # scale=descriptionと同一

        if isinstance(task_dict["test_data"], pd.DataFrame):
            for _, row in task_dict["test_data"].iterrows():
                # ここで、適切なカラム名や値の取り出し方に置き換える
                text = row.iloc[0]  # もしくは row['text']
                cur.execute("""
                    INSERT INTO test_data (task_id, data)
                    VALUES (%s, %s)
                """, (task_id, text))

        if isinstance(task_dict["data"], pd.DataFrame):
            for _, row in task_dict["data"].iterrows():
                # ここで、適切なカラム名や値の取り出し方に置き換える
                text = row.iloc[0]  # もしくは row['text']
                cur.execute("""
                    INSERT INTO annotation_data (task_id, data)
                    VALUES (%s, %s)
                """, (task_id, text))

        conn.commit()
        # 6. test_details テーブルにレコードを挿入
        test_ids = get_ids_by_task_id(task_id, "test_data")
        if test_ids is not None:
            success = set_test_data(test_ids, task_dict["user_id"], len(task_dict["questions"]))
            if not success:
                print("test_detailsの保存に失敗しました")
                return False
        
        # 7. annotation_details テーブルにレコードを挿入
        annotation_ids = get_ids_by_task_id(task_id, "annotation_data")
        if annotation_ids is not None:
            success = set_annotation_data(annotation_ids, len(task_dict["questions"]))
            if not success:
                print("annotation_detailsの保存に失敗しました")
                return False
            
        return task_id

    except Exception as e:
        if conn:
            conn.rollback()
        print(f"保存中にエラーが発生しました: {e}")
        return False

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
